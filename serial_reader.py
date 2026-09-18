"""Read sensor data from AirQino device via serial connection.

The AirQino REV6 board (gen-2022, by Quantit) does NOT have a USB port.
Connect using a USB-to-TTL serial adapter (CP2102 or FT232RL recommended)
wired to the board's TX/RX pins. Set adapter to 3.3V logic level.

Wiring:
    AirQino TX  -> Adapter RX
    AirQino GND -> Adapter GND
    Do NOT connect VCC (board has its own power supply).

The adapter appears as /dev/tty.usbserial-* (macOS) or /dev/ttyUSB* (Linux).
Set SERIAL_PORT in .env to this device path.
"""

import json
import re
import threading
import time
from collections import deque
from datetime import datetime, timezone


class SerialReader:
    """Reads and parses AirQino sensor data from a serial port.

    The AirQino sensor board outputs a semicolon-delimited text string
    containing raw sensor values at ~2-3 minute intervals.
    """

    # Known sensor field names in AirQino serial output
    KNOWN_FIELDS = {
        "co", "co2", "no2", "o3", "pm10", "pm25", "pm2.5",
        "rh", "extT", "intT", "voc", "lat", "lon",
        "ch2o", "h2s", "nh3", "so2", "noise",
    }

    def __init__(self, port, baud=9600, history_size=1000):
        self.port = port
        self.baud = baud
        self.history = deque(maxlen=history_size)
        self.latest = {}
        self._thread = None
        self._running = False
        self._serial = None

    def start(self):
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._read_loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False
        if self._serial:
            try:
                self._serial.close()
            except Exception:
                pass

    def _read_loop(self):
        import serial
        try:
            self._serial = serial.Serial(self.port, self.baud, timeout=5)
        except Exception as e:
            self.latest = {"error": str(e)}
            self._running = False
            return

        buffer = ""
        while self._running:
            try:
                raw = self._serial.readline()
                if not raw:
                    continue
                line = raw.decode("utf-8", errors="replace").strip()
                if not line:
                    continue
                parsed = self._parse_line(line)
                if parsed:
                    parsed["timestamp"] = datetime.now(timezone.utc).isoformat()
                    parsed["raw_line"] = line
                    self.latest = parsed
                    self.history.append(parsed)
            except Exception:
                time.sleep(1)

    def _parse_line(self, line):
        """Try to parse an AirQino sensor output line.

        AirQino outputs vary by firmware version. Common formats:
        - Semicolon-delimited: "co;no2;o3;pm10;pm25;rh;extT;intT;co2;voc"
        - Key=value pairs: "co=235;no2=17;o3=17;pm10=25;pm25=13"
        - JSON: {"co": 235, "no2": 17, ...}
        """
        # Try JSON first
        if line.startswith("{"):
            try:
                data = json.loads(line)
                return self._normalize(data)
            except json.JSONDecodeError:
                pass

        # Try key=value pairs (semicolon or comma separated)
        if "=" in line:
            data = {}
            for sep in [";", ","]:
                parts = line.split(sep)
                for part in parts:
                    if "=" in part:
                        k, _, v = part.partition("=")
                        k = k.strip().lower()
                        try:
                            data[k] = float(v.strip())
                        except ValueError:
                            data[k] = v.strip()
            if data:
                return self._normalize(data)

        # Try pure numeric semicolon-delimited (needs header mapping)
        parts = line.split(";")
        if len(parts) >= 5:
            try:
                values = [float(p.strip()) for p in parts if p.strip()]
                if len(values) >= 5:
                    # Best-effort field assignment based on common AirQino order
                    field_order = ["co", "no2", "o3", "pm10", "pm25",
                                   "rh", "extT", "intT", "co2", "voc"]
                    data = {}
                    for i, val in enumerate(values):
                        if i < len(field_order):
                            data[field_order[i]] = val
                    return self._normalize(data)
            except ValueError:
                pass

        return None

    def _normalize(self, data):
        """Normalize field names to consistent format."""
        normalized = {}
        mapping = {
            "pm2.5": "pm25", "pm2_5": "pm25",
            "extt": "extT", "ext_t": "extT", "temperature": "extT",
            "intt": "intT", "int_t": "intT",
            "humidity": "rh",
        }
        for k, v in data.items():
            key = mapping.get(k.lower(), k.lower() if k.lower() in self.KNOWN_FIELDS else k)
            normalized[key] = v
        return normalized

    def get_current(self):
        """Return the latest reading."""
        return dict(self.latest) if self.latest else None

    def get_history(self, limit=100):
        """Return recent readings."""
        items = list(self.history)
        return items[-limit:]
