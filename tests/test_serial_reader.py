"""The serial reader: the line parser, the reader thread and its accessors.

Phase 3 of docs/planning/test-suite-plan.md (T3.1-T3.7). The REV6 board has no USB
port, so the first live data will come through a USB-to-TTL adapter and this module.
What the board actually prints is unknown: the formats _parse_line accepts are
guesses (its docstring), and no capture exists yet.

T3.6 runs the real thread and real pyserial over a pseudo-terminal. D1 (plan §4) was
fixed in Session 14; its test is the last one here.
"""

import os
import time
from datetime import datetime, timedelta

import pytest

from serial_reader import SerialReader


def unstarted(**kwargs):
    """A reader whose thread never runs, so nothing opens the port."""
    return SerialReader("never-opened", **kwargs)


def poll(condition, deadline=2.0):
    """Wait for a condition the reader thread sets, without a fixed sleep."""
    end = time.monotonic() + deadline
    while not condition():
        if time.monotonic() > end:
            return False
        time.sleep(0.01)
    return True


# T3.1
@pytest.mark.parametrize("line, parsed", [
    pytest.param('{"co": 235, "no2": 17}', {"co": 235, "no2": 17}, id="json"),
    pytest.param('{"pm2.5": 7, "Temperature": 21.5, "humidity": 40}',
                 {"pm25": 7, "extT": 21.5, "rh": 40}, id="json-aliases"),
    pytest.param("co=1.5,pm25=7", {"co": 1.5, "pm25": 7.0}, id="comma-key-value"),
    pytest.param("co=235;no2=17;o3=17;pm10=25;pm25=13",  # the docstring's own example
                 {"co": 235.0, "no2": 17.0, "o3": 17.0, "pm10": 25.0, "pm25": 13.0},
                 id="semicolon-key-value"),
    # D1's mirror image: a ; in a comma line must not end up inside a value.
    pytest.param("co=1.5,pm25=7;", {"co": 1.5, "pm25": 7.0}, id="trailing-separator"),
    pytest.param("1;2;3;4;5;6;7;8;9;10",
                 {"co": 1.0, "no2": 2.0, "o3": 3.0, "pm10": 4.0, "pm25": 5.0,
                  "rh": 6.0, "extT": 7.0, "intT": 8.0, "co2": 9.0, "voc": 10.0},
                 id="ten-values-in-field-order"),
    pytest.param("1;2;3;4;5", {"co": 1.0, "no2": 2.0, "o3": 3.0, "pm10": 4.0, "pm25": 5.0},
                 id="five-values"),
    pytest.param("1;2;3;4", None, id="four-values"),
    pytest.param("1;2;x;4;5", None, id="non-numeric-token"),
    pytest.param("hello world", None, id="plain-text"),
    pytest.param('{"co": 1', None, id="malformed-json"),
])
def test_parse_line(line, parsed):
    assert unstarted()._parse_line(line) == parsed


# T3.2 — the mapping in _normalize (serial_reader.py:143-148)
@pytest.mark.parametrize("alias, field", [
    ("pm2.5", "pm25"), ("pm2_5", "pm25"),
    ("extt", "extT"), ("ext_t", "extT"), ("temperature", "extT"),
    ("intt", "intT"), ("int_t", "intT"),
    ("humidity", "rh"),
])
def test_normalize_maps_alias(alias, field):
    assert unstarted()._normalize({alias: 1.0}) == {field: 1.0}


def test_normalize_lowercases_known_fields():
    assert unstarted()._normalize({"CO": 1, "NO2": 2, "PM10": 3, "Rh": 4}) == {
        "co": 1, "no2": 2, "pm10": 3, "rh": 4}


def test_normalize_keeps_the_case_of_unknown_keys():
    assert unstarted()._normalize({"Foo": 1}) == {"Foo": 1}


# T3.3
def test_current_is_none_before_any_reading():
    assert unstarted().get_current() is None


def test_current_is_a_copy():
    reader = unstarted()
    reader.latest = {"co": 1.5}
    reader.get_current()["co"] = 99
    assert reader.latest == {"co": 1.5}


# T3.4
def test_history_returns_the_last_n():
    reader = unstarted()
    reader.history.extend({"i": i} for i in range(5))
    assert reader.get_history(2) == [{"i": 3}, {"i": 4}]


def test_history_drops_the_oldest_past_history_size():
    reader = unstarted(history_size=3)
    reader.history.extend({"i": i} for i in range(5))
    assert reader.get_history() == [{"i": 2}, {"i": 3}, {"i": 4}]


# T3.5
def test_start_is_idempotent():
    reader = unstarted()
    reader._read_loop = lambda: None  # a thread target that opens no port
    reader.start()
    first = reader._thread
    reader.start()
    assert first is not None
    assert reader._thread is first


# T3.6
@pytest.fixture
def pty_port():
    """A pseudo-terminal: the reader opens the slave end by name, the test writes to the master."""
    master, slave = os.openpty()
    yield master, os.ttyname(slave)
    os.close(master)
    os.close(slave)


@pytest.mark.skipif(not hasattr(os, "openpty"), reason="needs a POSIX pseudo-terminal")
def test_reader_thread_reads_a_real_tty(pty_port):
    master, port = pty_port
    reader = SerialReader(port)
    reader.start()
    try:
        # pyserial flushes input when it opens the port, so write only after that.
        assert poll(lambda: reader._serial is not None), "the reader never opened the port"
        os.write(master, b"!!noise!!\r\n")
        os.write(master, b"co=1.5,pm25=7\r\n")
        assert poll(lambda: reader.get_current() is not None), "no reading arrived"
    finally:
        reader.stop()  # never join(): readline blocks for up to 5 s (serial_reader.py:65)
    current = reader.get_current()
    assert (current["co"], current["pm25"]) == (1.5, 7.0)
    assert current["raw_line"] == "co=1.5,pm25=7"
    assert datetime.fromisoformat(current["timestamp"]).utcoffset() == timedelta(0)
    # The noise line went in first, so it was read and dropped before the reading.
    assert reader.get_history() == [current]


# T3.7
def test_open_failure_is_recorded_and_stops_the_reader(tmp_path):
    reader = SerialReader(str(tmp_path / "no-such-port"))
    reader.start()
    assert poll(lambda: reader.error and not reader._running)
    assert "no-such-port" in reader.error
    assert reader.get_current() is None  # the error is not a reading (D7)


# D1 (plan §4): the parser split a ;-joined line on , as well, and that second pass
# overwrote the first key with the rest of the line.
def test_semicolon_key_value_line_keeps_its_first_key():
    assert unstarted()._parse_line("co=235;no2=17")["co"] == 235.0
