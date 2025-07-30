# Device Code Configuration Steps

#### **Install Python Dependencies**

`pip install AWSIoTPythonSDK schedule boto3`

#### **Configure Certificates**

* Place the AWS IoT security certificates in a secure directory:  
  * `RootCA.pem`  
  * `certificate.pem.crt`  
  * `private.pem.key`

Update the file paths in the device script (`Feeder.py`):

`MQTT_CLIENT.configureEndpoint("your-endpoint.amazonaws.com", 8883)`  
`MQTT_CLIENT.configureCredentials("/path/to/RootCA.pem", "/path/to/private.pem.key", "/path/to/certificate.pem.crt")`

#### **Connect the Hardware**

* Connect the servo motor and other components to the Raspberry Pi GPIO pins as follows:  
  * **Servo Signal Pin**: GPIO 18 (or your selected GPIO pin)  
  * **Power (5V)**: 5V pin on the Raspberry Pi  
  * **Ground (GND)**: GND pin on the Raspberry Pi

#### **Running the Script** **`cd /path/to/smart-fish-feeder/deviceCode`**

Run the device script:  
`python3 Feeder.py`
