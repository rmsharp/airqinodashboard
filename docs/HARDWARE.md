# AirQino Hardware Connection Guide

## Device Identification

| Field | Value |
|-------|-------|
| **Product** | AirQino Air Aware Outdoor |
| **Part Number** | TEA 800506 |
| **Serial Number** | AIRO 6153 |
| **Board Revision** | REV6 (gen-2022) |
| **Firmware** | Net Rev3.11 |
| **Board Manufacturer** | Quantit (www.quantit.it) |
| **Product Manufacturer** | TEA Group, Signa (Florence), Italy |
| **Research Origin** | CNR-IBE (National Research Council, Institute of BioEconomy) |

## Internal Layout

The device contains three boards inside a weatherproof ABS enclosure (IP44):

| Board | Description |
|-------|-------------|
| **AirQino REV6** | Main sensor/controller board. Custom PCB with integrated ATmega microcontroller, all environmental sensors, and data processing. Silkscreen: "AirQino REV6 gen-2022 AIRQino MN-PW 11-2021 Rev6 Net Rev3.11" |
| **Second large board** | Power/interface board |
| **Cellular module** | SIM-based modem (GPRS/3G/4G) for cloud data transmission |

Other visible components:
- **GPS module** — small green board labeled "GPS"
- **Antenna (1595)** — small square tan module for GPS/cellular
- **LED indicator** — status light for power, modem, SD card, and GSM connection

## No USB Port

**The AirQino REV6 does NOT have a USB port.** Earlier revisions used a standard Arduino Mega 2560 (which has a USB-B port), but the REV6 is a custom PCB by Quantit with the microcontroller integrated directly onto the board. The USB-B port was eliminated in this redesign.

## Connecting for Local Data Access

### Option 1: USB-to-TTL Serial Adapter (Recommended)

The board exposes **TX/RX pins** for serial communication. You need a USB-to-TTL adapter to bridge these pins to your computer's USB port.

#### Recommended Adapters

Any CP2102 or FT232RL-based adapter will work. These are macOS-compatible and support 3.3V logic:

**Best options (verified in stock as of April 2026):**

- **DSD TECH SH-U09C5** (~$12, Amazon) — Genuine FTDI FT232RL chip. Cable form factor with 4-pin DuPont wires included. Supports 1.8V/2.5V/3.3V/5V via selector. macOS plug-and-play. **Recommended — no extra parts needed.**
- **SparkFun FTDI Basic Breakout 3.3V** ($14.95, sparkfun.com) — Genuine FTDI chip, dedicated 3.3V board. Product DEV-09873. Needs separate jumper wires.
- **DSD TECH CP2102 with DuPont cable** (~$8, Amazon) — CP2102 chip, 3.3V and 5V pins, includes jumper wires. Budget option.

**Note:** Some cheap adapters use counterfeit FTDI chips that can cause driver issues. DSD TECH and SparkFun products use genuine chips. CP2102-based adapters (Silicon Labs) don't have this problem.

#### Wiring

```
AirQino REV6 Board          USB-to-TTL Adapter
──────────────────          ──────────────────
TX  ───────────────────────→  RX
GND ───────────────────────→  GND

Do NOT connect:
- VCC/5V (the AirQino has its own power supply)
- RX to TX (only needed if sending commands TO the board)
```

**Voltage:** The board shows 3.0V and 3.4V power rails. Set your adapter to **3.3V** logic level (most adapters have a jumper or switch).

**You will also need 2-3 female-to-female dupont jumper wires** to connect the adapter pins to the AirQino board's pin headers (TX, RX, GND). Most adapters do not include these. They are sold in packs on Amazon — search "female to female dupont jumper wires."

#### Software Setup

Once the adapter is plugged into your Mac, it appears as a serial device:

```bash
# Find the device name
ls /dev/tty.usb*

# Configure in .env
SERIAL_PORT=/dev/tty.usbserial-XXXX
SERIAL_BAUD=9600
```

Then start the dashboard:

```bash
python3 app.py
# Open http://localhost:5001
```

The serial reader will automatically parse the AirQino's sensor output (semicolon-delimited text, key=value pairs, or JSON depending on firmware version).

### Option 2: SD Card

The device has an onboard SD card (confirmed by LED diagnostics at startup). The SD card logs sensor data locally.

To access:
1. Power off the device
2. Locate the SD card slot (may be between stacked boards or on the underside of the main board)
3. Remove the SD card
4. Read it on your computer
5. Upload the data file through the dashboard's CSV upload feature at http://localhost:5001

### Option 3: Cloud API

The device transmits data via its cellular module to the AirQino cloud platform. To access this data via the API:

1. Contact **info@airqino.it** or **info@tea-group.it** with serial number **AIRO 6153**
2. Request OAuth2 API credentials (client ID, client secret, username, password)
3. Ask for your station's `SMART###` name (the serial number doesn't map directly to the API station name)
4. Configure credentials in `.env` (see `.env.example`)

## LED Status Indicators

At power-on, the device LED indicates system health:

| Flash Pattern | Timing | Component | Meaning |
|--------------|--------|-----------|---------|
| 1 flash/sec | On connection | Power supply | OK — starting up |
| 5 flashes/sec | After 10 sec | Modem, SD card, internal memory | FAIL — component error |
| 1 flash/sec | After 10 sec | GSM connection | Searching for network |
| 5 flashes/sec | After 10 min | GSM connection | FAIL — no network found |

## Board Pin Markings

Markings visible on the AirQino REV6 board:

```
GPS   DATA   PWR   GND   VCC   5V   3.4V   3.0V   TX/RX
```

- **TX/RX** — Serial data output/input (connect USB-to-TTL adapter here)
- **DATA** — Data bus (used internally)
- **PWR** — Power input
- **GND** — Ground (connect to adapter GND)
- **VCC, 5V, 3.4V, 3.0V** — Voltage rails (do not connect external power)
- **GPS** — GPS module connection

## Specifications

| Parameter | Value |
|-----------|-------|
| Power | 110/230 VAC, 50/60 Hz, 5W |
| Operating temp | -30 to +70 C |
| Operating humidity | 0-100% RH |
| Enclosure | ABS, IP44 |
| Dimensions | 205 x 220 mm |
| Weight | 0.9 kg |
| Communication | Cellular (GPRS/3G/4G), optional RS-232, optional Ethernet |
| Data storage | SD card + cloud |
| Sensors | PM2.5, PM10, NO2, O3, CO, CO2, temperature, humidity, VOC |
| Calibration | Factory calibrated; recalibration recommended every 2 years |
| Maintenance | Sensor cleaning every 6 months (environment-dependent) |

## References

- [AirQino User Manual (Scribd)](https://www.scribd.com/document/626867215/Airqino-Manual)
- [TEA Group AirQino Catalog (PDF)](https://www.tea-group.it/wp-content/uploads/2020/10/CATALOGO-AIRQINO-INGLESE.pub_.pdf)
- [AirQino on Snap4City (CNR-IBE)](https://www.snap4city.org/drupal/node/508)
- [AirQino specs (Clean Air Stars)](https://monitors.cleanairstars.com/upcp_product/oudoor-airquino/)
- [TEA 800506 Instruction Manual](https://all-guidesbox.com/manual/1968456/tea-airqino-air-aware-instruction-manual-10.html)
