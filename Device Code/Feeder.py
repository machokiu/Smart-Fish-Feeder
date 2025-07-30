import json
import time
import schedule
import boto3
from datetime import datetime, timezone, timedelta
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import RPi.GPIO as GPIO

# Define GPIO Pin for the servo motor
SERVO_PIN = 18

# MQTT Configuration
ENDPOINT = ***
CLIENT_ID = "FishFeeder"
PATH_TO_CERT = ***
PATH_TO_KEY = ***
PATH_TO_ROOT_CA = ***
TOPIC_FEED_NOW = "iot/commands/feed-now"
TOPIC_UPDATE_SCHEDULE = "iot/commands/update-schedule"
TOPIC_FEED_LOG = "iot/commands/feed-log"

# Define PST timezone
PST = timezone(timedelta(hours=-8))

# Servo motor setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)
pwm = GPIO.PWM(SERVO_PIN, 50)  # 50Hz frequency
pwm.start(0)  # Initialize servo motor

# Local schedule storage
feeding_schedule = []


# Function to rotate servo motor
def rotate_servo():
    print("Rotating servo motor...")
    pwm.ChangeDutyCycle(3)
    time.sleep(4)
    pwm.ChangeDutyCycle(12)


# Handle feed-now topic
def on_feed_now(client, userdata, message):
    print("Received feed-now message.")
    payload = json.loads(message.payload)
    rotate_servo()
    send_feed_log(method="manual")


# Handle update-schedule topic
def on_update_schedule(client, userdata, message):
    global feeding_schedule
    print("Received update schedule message.")
    payload = json.loads(message.payload)

    # Update the local schedule with the new schedule
    feeding_schedule = payload.get("schedules", [])
    print(f"Updated feeding schedule: {feeding_schedule}")

    # Clear previous jobs and reschedule
    schedule.clear()
    for schedule_item in feeding_schedule:
        time_str = schedule_item['time']
        days = schedule_item['days']
        for day in days:
            schedule.every().day.at(time_str).do(schedule_feeding, day=day).tag(f"{day}_{time_str}")


# Function to execute scheduled feeding
def schedule_feeding(day):
    current_time = datetime.now(PST)
    if current_time.strftime('%a') == day:
        print(f"Scheduled feeding triggered for {day}.")
        rotate_servo()
        send_feed_log(method="schedule")


# Publish feeding log
def send_feed_log(method):
    current_time = datetime.now(PST).strftime('%Y-%m-%d %H:%M:%S')
    log_entry = {
        "id": str(int(time.time() * 1000)),
        "time": current_time,
        "method": method
    }
    mqtt_client.publish(TOPIC_FEED_LOG, json.dumps(log_entry), 1)
    print(f"Published feeding log: {log_entry}")


# Initialize MQTT Client
mqtt_client = AWSIoTMQTTClient(CLIENT_ID)
mqtt_client.configureEndpoint(ENDPOINT, 8883)
mqtt_client.configureCredentials(PATH_TO_ROOT_CA, PATH_TO_KEY, PATH_TO_CERT)
mqtt_client.configureAutoReconnectBackoffTime(1, 32, 20)
mqtt_client.configureOfflinePublishQueueing(-1)  # Infinite offline publish queueing
mqtt_client.configureDrainingFrequency(2)  # Draining: 2 Hz
mqtt_client.configureConnectDisconnectTimeout(10)
mqtt_client.configureMQTTOperationTimeout(10)

# Connect to AWS IoT
mqtt_client.connect()

# Subscribe to topics
mqtt_client.subscribe(TOPIC_FEED_NOW, 1, on_feed_now)
mqtt_client.subscribe(TOPIC_UPDATE_SCHEDULE, 1, on_update_schedule)

print("Subscribed to topics and waiting for messages...")

# Main loop
try:
    while True:
        schedule.run_pending()  # Check for scheduled jobs
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting...")
    pwm.stop()
    GPIO.cleanup()
