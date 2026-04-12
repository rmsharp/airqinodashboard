/* AirQino Dashboard — client-side logic */

// --- AQI thresholds (EPA breakpoints) ---
const AQI = {
    pm25: [
        { max: 12, cls: 'aqi-good' },
        { max: 35.4, cls: 'aqi-moderate' },
        { max: 55.4, cls: 'aqi-usg' },
        { max: 150.4, cls: 'aqi-unhealthy' },
        { max: 250.4, cls: 'aqi-very-unhealthy' },
        { max: Infinity, cls: 'aqi-hazardous' },
    ],
    pm10: [
        { max: 54, cls: 'aqi-good' },
        { max: 154, cls: 'aqi-moderate' },
        { max: 254, cls: 'aqi-usg' },
        { max: 354, cls: 'aqi-unhealthy' },
        { max: 424, cls: 'aqi-very-unhealthy' },
        { max: Infinity, cls: 'aqi-hazardous' },
    ],
    no2: [
        { max: 53, cls: 'aqi-good' },
        { max: 100, cls: 'aqi-moderate' },
        { max: 360, cls: 'aqi-usg' },
        { max: 649, cls: 'aqi-unhealthy' },
        { max: 1249, cls: 'aqi-very-unhealthy' },
        { max: Infinity, cls: 'aqi-hazardous' },
    ],
    o3: [
        { max: 54, cls: 'aqi-good' },
        { max: 70, cls: 'aqi-moderate' },
        { max: 85, cls: 'aqi-usg' },
        { max: 105, cls: 'aqi-unhealthy' },
        { max: 200, cls: 'aqi-very-unhealthy' },
        { max: Infinity, cls: 'aqi-hazardous' },
    ],
    co: [
        { max: 4.4, cls: 'aqi-good' },
        { max: 9.4, cls: 'aqi-moderate' },
        { max: 12.4, cls: 'aqi-usg' },
        { max: 15.4, cls: 'aqi-unhealthy' },
        { max: 30.4, cls: 'aqi-very-unhealthy' },
        { max: Infinity, cls: 'aqi-hazardous' },
    ],
};

const SENSOR_META = {
    pm25:  { label: 'PM2.5',       unit: '\u00b5g/m\u00b3', color: '#6c8cff' },
    pm10:  { label: 'PM10',        unit: '\u00b5g/m\u00b3', color: '#a78bfa' },
    no2:   { label: 'NO\u2082',    unit: '\u00b5g/m\u00b3', color: '#fb923c' },
    co:    { label: 'CO',          unit: 'mg/m\u00b3',      color: '#f87171' },
    o3:    { label: 'O\u2083',     unit: '\u00b5g/m\u00b3', color: '#34d399' },
    co2:   { label: 'CO\u2082',    unit: 'ppm',             color: '#fbbf24' },
    extT:  { label: 'Temperature', unit: '\u00b0C',         color: '#f472b6' },
    rh:    { label: 'Humidity',    unit: '%',               color: '#38bdf8' },
    voc:   { label: 'VOC',         unit: '\u00b5g/m\u00b3', color: '#818cf8' },
};

const FIELD_ALIASES = {
    'pm2.5': 'pm25', 'PM2.5': 'pm25', 'PM25': 'pm25', 'pm2_5': 'pm25',
    'PM10': 'pm10', 'Pm10': 'pm10',
    'NO2': 'no2', 'No2': 'no2',
    'CO': 'co', 'Co': 'co',
    'O3': 'o3',
    'CO2': 'co2', 'Co2': 'co2',
    'T': 'extT', 'temperature': 'extT', 'temp': 'extT', 'extt': 'extT',
    'intt': 'intT',
    'RH': 'rh', 'humidity': 'rh',
    'VOC': 'voc', 'Voc': 'voc',
};

function normalize(key) {
    return FIELD_ALIASES[key] || key.toLowerCase();
}

function aqiClass(sensor, value) {
    const table = AQI[sensor];
    if (!table || value == null) return '';
    for (const row of table) {
        if (value <= row.max) return row.cls;
    }
    return '';
}

// --- Chart.js ---
let chart = null;
let activeSensors = new Set(['pm25', 'pm10']);
let chartRange = 24;

function initChart() {
    const ctx = document.getElementById('mainChart');
    if (!ctx) return;
    chart = new Chart(ctx, {
        type: 'line',
        data: { datasets: [] },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: { mode: 'index', intersect: false },
            plugins: {
                legend: {
                    display: true,
                    labels: { color: '#8b8fa3', font: { size: 11 }, boxWidth: 12 },
                },
                tooltip: {
                    backgroundColor: '#232734',
                    titleColor: '#e4e6ed',
                    bodyColor: '#e4e6ed',
                    borderColor: '#2e3345',
                    borderWidth: 1,
                },
            },
            scales: {
                x: {
                    type: 'time',
                    time: {
                        tooltipFormat: 'MMM d, HH:mm',
                        displayFormats: { hour: 'HH:mm', day: 'MMM d' },
                    },
                    grid: { color: '#2e3345' },
                    ticks: { color: '#8b8fa3', font: { size: 10 }, maxTicksLimit: 12 },
                },
                y: {
                    grid: { color: '#2e3345' },
                    ticks: { color: '#8b8fa3', font: { size: 10 } },
                },
            },
        },
    });
}

// --- Data fetching ---

async function fetchJSON(url) {
    const resp = await fetch(url);
    if (!resp.ok) {
        const body = await resp.json().catch(() => ({}));
        throw new Error(body.error || 'HTTP ' + resp.status);
    }
    return resp.json();
}

async function loadCurrent() {
    try {
        const result = await fetchJSON('/api/current');
        renderReadings(result);
    } catch (e) {
        console.warn('loadCurrent:', e.message);
    }
}

async function loadTimeseries() {
    try {
        const result = await fetchJSON('/api/timeseries?hours=' + chartRange);
        renderChart(result);
    } catch (e) {
        console.warn('loadTimeseries:', e.message);
    }
}

async function loadMetadata() {
    try {
        const result = await fetchJSON('/api/metadata');
        renderMetadata(result);
    } catch (e) {
        console.warn('loadMetadata:', e.message);
    }
}

// --- Rendering ---

function renderReadings(result) {
    const grid = document.getElementById('readingsGrid');
    if (!grid) return;

    let values = {};
    let timestamp = '';
    const data = result.data;
    if (!data) return;

    if (result.source === 'api') {
        timestamp = data.timestamp || '';
        if (Array.isArray(data.values)) {
            for (const v of data.values) {
                values[normalize(v.sensor)] = v.value;
            }
        } else if (typeof data === 'object') {
            timestamp = data.utc_timestamp || data.timestamp || '';
            for (const [k, v] of Object.entries(data)) {
                const key = normalize(k);
                if (SENSOR_META[key]) values[key] = v;
            }
        }
    } else {
        timestamp = data.timestamp || '';
        for (const [k, v] of Object.entries(data)) {
            const key = normalize(k);
            if (SENSOR_META[key] && typeof v === 'number') values[key] = v;
        }
        // Update map from CSV lat/lon if available
        var lat = data.lat || data.latitude;
        var lon = data.lon || data.longitude;
        if (lat && lon) updateMap(lat, lon, 'AIRO 6153');
    }

    const order = ['pm25', 'pm10', 'no2', 'co', 'o3', 'co2', 'extT', 'rh', 'voc'];
    let html = '';
    for (const sensor of order) {
        const meta = SENSOR_META[sensor];
        const val = values[sensor];
        if (val == null) continue;
        const cls = aqiClass(sensor, val);
        const displayVal = typeof val === 'number' ? (val % 1 === 0 ? val : val.toFixed(1)) : val;
        html += '<div class="reading-card ' + cls + '">'
            + '<div class="label">' + meta.label + '</div>'
            + '<div class="value">' + displayVal + '<span class="unit">' + meta.unit + '</span></div>'
            + (timestamp ? '<div class="timestamp">' + formatTime(timestamp) + '</div>' : '')
            + '<div class="bar"></div>'
            + '</div>';
    }
    grid.innerHTML = html || '<div class="placeholder">No readings available</div>';
}

function renderChart(result) {
    if (!chart) return;
    const data = result.data;
    if (!data || !Array.isArray(data)) {
        chart.data.datasets = [];
        chart.update();
        return;
    }

    const datasets = [];
    for (const sensor of activeSensors) {
        const meta = SENSOR_META[sensor];
        if (!meta) continue;
        const points = [];

        for (const row of data) {
            let ts, val;
            if (result.source === 'api') {
                if (row.sensor) {
                    if (normalize(row.sensor) !== sensor) continue;
                    ts = row.timestamp_utc || row.utc_timestamp || row.timestamp;
                    val = row.calibrated_value != null ? row.calibrated_value : row.raw_value;
                } else {
                    ts = row.utc_timestamp || row.timestamp;
                    val = row[sensor] ?? row[sensor.toUpperCase()] ?? row[meta.label];
                }
            } else {
                ts = row.timestamp;
                // CSV data has lowercase keys; try direct, then scan with normalization
                val = row[sensor];
                if (val == null) {
                    for (var rk in row) {
                        if (normalize(rk) === sensor) { val = row[rk]; break; }
                    }
                }
            }
            if (ts && val != null) {
                const tStr = ts.includes('T') ? ts : ts.replace(' ', 'T');
                const tFull = tStr.includes('Z') || tStr.includes('+') ? tStr : tStr + 'Z';
                points.push({ x: new Date(tFull), y: parseFloat(val) });
            }
        }

        if (points.length > 0) {
            points.sort((a, b) => a.x - b.x);
            datasets.push({
                label: meta.label,
                data: points,
                borderColor: meta.color,
                backgroundColor: meta.color + '20',
                borderWidth: 1.5,
                pointRadius: 0,
                pointHoverRadius: 4,
                tension: 0.3,
                fill: true,
            });
        }
    }

    chart.data.datasets = datasets;
    chart.update();
}

function renderMetadata(result) {
    const panel = document.getElementById('metadataPanel');
    if (!panel) return;

    const info = result.session_info || {};
    const fields = [
        ['Station', info.station || '\u2014'],
        ['Description', info.description || '\u2014'],
        ['Session ID', info.sessiond_id || info.session_id || '\u2014'],
    ];

    if (info.latitude || info.lat) {
        const lat = info.latitude || info.lat;
        const lon = info.longitude || info.lon;
        fields.push(['GPS', lat + ', ' + lon]);
        updateMap(lat, lon, info.station || '');
    }

    if (Array.isArray(info.integrated_sensors)) {
        const list = info.integrated_sensors.map(function(s) { return s.type + ' (' + s.unit + ')'; }).join(', ');
        fields.push(['Sensors', list]);
    }

    for (const key of ['aux-1', 'aux-2', 'aux-3', 'aux-4', 'aux-5']) {
        if (info[key] && info[key].type) {
            fields.push([key.toUpperCase(), info[key].type + ' (' + info[key].unit + ')']);
        }
    }

    if (info.activation_date) {
        fields.push(['Activated', info.activation_date]);
    }

    let html = '';
    for (const [k, v] of fields) {
        const dv = typeof v === 'string' && v.length > 60 ? v.substring(0, 57) + '...' : v;
        html += '<div class="meta-row"><span class="key">' + k + '</span><span class="val">' + dv + '</span></div>';
    }
    panel.innerHTML = html || '<div class="placeholder">No metadata available</div>';
}

// --- Map ---
let map = null;
let marker = null;

function initMap() {
    const el = document.getElementById('map');
    if (!el || typeof L === 'undefined') return;
    map = L.map('map', { zoomControl: false }).setView([43.0, 11.0], 6);
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; OpenStreetMap &copy; CARTO',
        maxZoom: 19,
    }).addTo(map);
    L.control.zoom({ position: 'bottomright' }).addTo(map);
}

function updateMap(lat, lon, label) {
    if (!map) return;
    const ll = [parseFloat(lat), parseFloat(lon)];
    if (marker) marker.setLatLng(ll);
    else marker = L.marker(ll).addTo(map);
    marker.bindPopup('<b>' + label + '</b><br>' + ll[0].toFixed(5) + ', ' + ll[1].toFixed(5));
    map.setView(ll, 14);
}

// --- Helpers ---

function formatTime(ts) {
    if (!ts) return '';
    try {
        const tStr = ts.includes('T') ? ts : ts.replace(' ', 'T');
        const tFull = tStr.includes('Z') || tStr.includes('+') ? tStr : tStr + 'Z';
        const d = new Date(tFull);
        return d.toLocaleString(undefined, { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
    } catch (e) {
        return ts;
    }
}

// --- Sensor toggles ---

function renderSensorToggles() {
    const container = document.getElementById('sensorToggles');
    if (!container) return;
    let html = '';
    for (const [key, meta] of Object.entries(SENSOR_META)) {
        const active = activeSensors.has(key) ? 'active' : '';
        const style = active ? 'border-color:' + meta.color + ';color:' + meta.color : '';
        html += '<button class="sensor-toggle ' + active + '" data-sensor="' + key + '" style="' + style + '">'
            + meta.label + '</button>';
    }
    container.innerHTML = html;
    container.querySelectorAll('.sensor-toggle').forEach(function(btn) {
        btn.addEventListener('click', function() {
            var s = btn.dataset.sensor;
            if (activeSensors.has(s)) activeSensors.delete(s);
            else activeSensors.add(s);
            renderSensorToggles();
            loadTimeseries();
        });
    });
}

// --- Range buttons ---

function setupRangeButtons() {
    document.querySelectorAll('.chart-controls button[data-hours]').forEach(function(btn) {
        btn.addEventListener('click', function() {
            document.querySelectorAll('.chart-controls button[data-hours]').forEach(function(b) {
                b.classList.remove('active');
            });
            btn.classList.add('active');
            chartRange = parseInt(btn.dataset.hours);
            loadTimeseries();
        });
    });
}

// --- CSV upload ---

function setupUpload() {
    const area = document.getElementById('uploadArea');
    const input = document.getElementById('csvInput');
    const status = document.getElementById('uploadStatus');
    if (!area || !input) return;

    area.addEventListener('click', function() { input.click(); });
    area.addEventListener('dragover', function(e) {
        e.preventDefault();
        area.style.borderColor = 'var(--accent)';
    });
    area.addEventListener('dragleave', function() {
        area.style.borderColor = '';
    });
    area.addEventListener('drop', function(e) {
        e.preventDefault();
        area.style.borderColor = '';
        if (e.dataTransfer.files.length > 0) uploadFile(e.dataTransfer.files[0]);
    });
    input.addEventListener('change', function() {
        if (input.files.length > 0) uploadFile(input.files[0]);
    });

    async function uploadFile(file) {
        const form = new FormData();
        form.append('file', file);
        try {
            const resp = await fetch('/api/upload_csv', { method: 'POST', body: form });
            const result = await resp.json();
            if (result.error) {
                status.textContent = 'Error: ' + result.error;
                status.style.color = 'var(--unhealthy)';
            } else {
                status.textContent = 'Loaded ' + result.rows + ' rows (' + result.columns.length + ' columns)';
                status.style.color = 'var(--good)';
                loadCurrent();
                loadTimeseries();
            }
        } catch (e) {
            status.textContent = 'Upload failed: ' + e.message;
            status.style.color = 'var(--unhealthy)';
        }
    }
}

// --- Refresh loop ---

let refreshInterval = null;

function startRefresh(intervalMs) {
    intervalMs = intervalMs || 60000;
    loadCurrent();
    loadTimeseries();
    loadMetadata();
    if (refreshInterval) clearInterval(refreshInterval);
    refreshInterval = setInterval(function() {
        loadCurrent();
    }, intervalMs);
}

// --- Init ---

document.addEventListener('DOMContentLoaded', function() {
    initChart();
    initMap();
    renderSensorToggles();
    setupRangeButtons();
    setupUpload();
    startRefresh();
});
