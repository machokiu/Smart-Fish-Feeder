# Smart Fish Feeder - Device Configuration

This document provides the configuration steps for setting up the **Raspberry Pi device** that controls the Smart Fish Feeder. The device communicates securely with AWS IoT Core, subscribes to feeding commands, executes feeding actions using a servo motor, and publishes feeding logs back to the cloud.

---

## 1️⃣ Install Python Dependencies

### On your Raspberry Pi, install the required Python libraries:

```bash
pip install AWSIoTPythonSDK schedule boto3 
```
---

## 2️⃣ Configure Certificates

1. Place the AWS IoT security certificates in a secure directory:  
  - `RootCA.pem`  
  - `certificate.pem.crt`  
  - `private.pem.key`

2. Update the file paths in the device script (`Feeder.py`):

- `MQTT_CLIENT.configureEndpoint("your-endpoint.amazonaws.com", 8883)`  
- `MQTT_CLIENT.configureCredentials("/path/to/RootCA.pem", "/path/to/private.pem.key", "/path/to/certificate.pem.crt")`

---

## 3️⃣ Connect the Hardware

### Connect the servo motor and other components to the Raspberry Pi GPIO pins as follows:
- **Servo Signal Pin**: GPIO 18 (or your selected GPIO pin)
- **Power (5V)**: 5V pin on the Raspberry Pi
- **Ground (GND)**: GND pin on the Raspberry Pi

---

## 4️⃣ Running the Script 
```bash
cd /path/to/smart-fish-feeder/deviceCode
python3 Feeder.py
```
