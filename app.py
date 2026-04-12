"""AirQino Environmental Monitoring Dashboard."""

import csv
import io
import json
import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-key-change-me")

# --- State ---

_api_client = None
_serial_reader = None
_csv_data = None  # Uploaded CSV data cache


def get_api_client():
    global _api_client
    if _api_client:
        return _api_client
    cid = os.getenv("AIRQINO_CLIENT_ID")
    csecret = os.getenv("AIRQINO_CLIENT_SECRET")
    user = os.getenv("AIRQINO_USERNAME")
    pwd = os.getenv("AIRQINO_PASSWORD")
    if cid and csecret and user and pwd:
        from airqino_client import AirQinoClient
        _api_client = AirQinoClient(cid, csecret, user, pwd)
    return _api_client


def get_serial_reader():
    global _serial_reader
    if _serial_reader:
        return _serial_reader
    port = os.getenv("SERIAL_PORT")
    baud = int(os.getenv("SERIAL_BAUD", "9600"))
    if port:
        from serial_reader import SerialReader
        _serial_reader = SerialReader(port, baud)
        _serial_reader.start()
    return _serial_reader


def active_source():
    """Return which data source is configured."""
    if os.getenv("AIRQINO_CLIENT_ID"):
        return "api"
    if os.getenv("SERIAL_PORT"):
        return "serial"
    if _csv_data:
        return "csv"
    return None


# --- Routes ---

@app.route("/")
def dashboard():
    station = os.getenv("AIRQINO_STATION_NAME", "")
    project = os.getenv("AIRQINO_PROJECT_NAME", "")
    source = active_source()
    return render_template("dashboard.html",
                           station_name=station,
                           project_name=project,
                           source=source)


@app.route("/api/status")
def api_status():
    """Return current configuration status."""
    source = active_source()
    station = os.getenv("AIRQINO_STATION_NAME", "")
    project = os.getenv("AIRQINO_PROJECT_NAME", "")
    serial_port = os.getenv("SERIAL_PORT", "")
    return jsonify({
        "source": source,
        "station_name": station,
        "project_name": project,
        "serial_port": serial_port,
        "has_csv": _csv_data is not None,
    })


@app.route("/api/stations")
def api_stations():
    """List stations for a project (API mode)."""
    client = get_api_client()
    if not client:
        return jsonify({"error": "API not configured"}), 503
    project = request.args.get("project", os.getenv("AIRQINO_PROJECT_NAME", ""))
    if not project:
        return jsonify({"error": "No project name specified"}), 400
    try:
        data = client.get_stations(project)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 502


@app.route("/api/metadata")
def api_metadata():
    """Station metadata: sensors, coordinates, description."""
    client = get_api_client()
    if not client:
        return jsonify({"error": "API not configured"}), 503
    station = request.args.get("station", os.getenv("AIRQINO_STATION_NAME", ""))
    project = request.args.get("project", os.getenv("AIRQINO_PROJECT_NAME", ""))
    try:
        result = {}
        if project:
            info = client.get_session_info(project)
            # Find our station in the project info
            if isinstance(info, list):
                for entry in info:
                    if entry.get("station") == station:
                        result["session_info"] = entry
                        break
                if not result.get("session_info") and info:
                    result["session_info"] = info[0]
            else:
                result["session_info"] = info
        if station:
            sensors = client.get_sensors(station)
            result["sensors"] = sensors
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 502


@app.route("/api/current")
def api_current():
    """Current sensor readings from whichever source is active."""
    # Try serial first (real-time)
    reader = get_serial_reader()
    if reader:
        data = reader.get_current()
        if data:
            return jsonify({"source": "serial", "data": data})
        return jsonify({"source": "serial", "data": None,
                        "error": "No data received yet"}), 202

    # Try API
    client = get_api_client()
    if client:
        station = request.args.get("station", os.getenv("AIRQINO_STATION_NAME", ""))
        if not station:
            return jsonify({"error": "No station name configured"}), 400
        try:
            data = client.get_current_values(station)
            return jsonify({"source": "api", "data": data})
        except Exception as e:
            return jsonify({"error": str(e)}), 502

    # CSV fallback — return the most recent row
    if _csv_data and len(_csv_data) > 0:
        return jsonify({"source": "csv", "data": _csv_data[-1]})

    return jsonify({"error": "No data source configured"}), 503


@app.route("/api/timeseries")
def api_timeseries():
    """Time-series data for charting."""
    hours = int(request.args.get("hours", 24))
    sensor = request.args.get("sensor", "")  # optional filter

    # Serial history
    reader = get_serial_reader()
    if reader:
        history = reader.get_history(limit=500)
        if sensor:
            history = [
                {**r, "values": {sensor: r.get(sensor)}}
                for r in history if sensor in r
            ]
        return jsonify({"source": "serial", "data": history})

    # API — last 12h via getLastStationData, or getRange for longer
    client = get_api_client()
    if client:
        station = request.args.get("station", os.getenv("AIRQINO_STATION_NAME", ""))
        if not station:
            return jsonify({"error": "No station name configured"}), 400
        try:
            if hours <= 12:
                data = client.get_last_station_data(station_name=station)
                return jsonify({"source": "api", "data": data})
            else:
                date_to = datetime.utcnow().strftime("%Y-%m-%d")
                date_from = (datetime.utcnow() - timedelta(hours=hours)).strftime("%Y-%m-%d")
                data = client.get_range(station, date_from, date_to)
                return jsonify({"source": "api", "data": data})
        except Exception as e:
            return jsonify({"error": str(e)}), 502

    # CSV data
    if _csv_data:
        data = _csv_data
        if sensor:
            data = [r for r in data if sensor in r]
        return jsonify({"source": "csv", "data": data[-500:]})

    return jsonify({"error": "No data source configured"}), 503


@app.route("/api/hourly")
def api_hourly():
    """Hourly averages for charting (API mode, pivoted)."""
    client = get_api_client()
    if not client:
        return jsonify({"error": "API not configured"}), 503
    station = request.args.get("station", os.getenv("AIRQINO_STATION_NAME", ""))
    days = int(request.args.get("days", 7))
    if not station:
        return jsonify({"error": "No station name configured"}), 400
    date_to = datetime.utcnow().strftime("%Y-%m-%d")
    date_from = (datetime.utcnow() - timedelta(days=days)).strftime("%Y-%m-%d")
    try:
        csv_text = client.get_hourly_avg(station, date_from, date_to, pivot=True)
        # Parse CSV to JSON
        reader = csv.DictReader(io.StringIO(csv_text), delimiter=";")
        rows = list(reader)
        return jsonify({"source": "api", "data": rows})
    except Exception as e:
        return jsonify({"error": str(e)}), 502


@app.route("/api/upload_csv", methods=["POST"])
def upload_csv():
    """Upload a CSV file from the AirQino SD card."""
    global _csv_data
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    f = request.files["file"]
    if not f.filename:
        return jsonify({"error": "No file selected"}), 400

    text = f.read().decode("utf-8", errors="replace")

    # Auto-detect delimiter
    first_line = text.split("\n")[0]
    if ";" in first_line:
        delimiter = ";"
    elif "\t" in first_line:
        delimiter = "\t"
    else:
        delimiter = ","

    reader = csv.DictReader(io.StringIO(text), delimiter=delimiter)
    rows = []
    for row in reader:
        cleaned = {}
        for k, v in row.items():
            k = k.strip().lower()
            try:
                cleaned[k] = float(v)
            except (ValueError, TypeError):
                cleaned[k] = v.strip() if isinstance(v, str) else v
        rows.append(cleaned)

    _csv_data = rows
    return jsonify({
        "rows": len(rows),
        "columns": list(rows[0].keys()) if rows else [],
    })


if __name__ == "__main__":
    print("\n  AirQino Dashboard: http://localhost:5001\n")
    app.run(host="0.0.0.0", port=5001, debug=True)
