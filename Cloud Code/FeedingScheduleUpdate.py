import boto3
import json
from datetime import datetime

s3 = boto3.client('s3')
iot = boto3.client('iot-data', region_name='us-west-2')
BUCKET_NAME = 'fish-feeder-logs'
MQTT_TOPIC = 'iot/commands/update-schedule'  # Topic for schedule updates

def lambda_handler(event, context):
    print(f"Event received: {json.dumps(event)}")  # Log the incoming event

    try:
        # Ensure 'body' exists and parse it
        if 'body' not in event:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing request body'})
            }

        body = json.loads(event['body'])  # Parse the body of the event
        action = body.get('action')  # Get the action value from the body

        # Validate the action field
        if not action:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Action is required'})
            }

        if action == 'update':
            return update_schedule(body)

        elif action == 'clear':
            return clear_schedules()

        else:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Invalid action'})
            }

    except Exception as e:
        print(f"Error handling feeding schedule: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal Server Error'})
        }

# Function to handle schedule update
def update_schedule(body):
    time = body.get('time')
    days = body.get('days')

    # Validate input
    if not time or not days:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Time and days are required for schedule update'})
        }

    # Fetch existing schedules to check for conflicts
    existing_schedules = get_existing_schedules()

    # Check for duplicate schedules
    for schedule in existing_schedules:
        if schedule['time'] == time and set(schedule['days']) == set(days):
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Duplicate schedule detected! This schedule already exists.'})
            }

    # Add the new schedule
    new_schedule = {
        'id': str(int(datetime.now().timestamp() * 1000)),  # Unique ID
        'time': time,
        'days': days
    }

    key = f"feeding-schedules/{new_schedule['id']}.json"
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=key,
        Body=json.dumps(new_schedule),
        ContentType='application/json'
    )

    # Consolidate all schedules (existing + new)
    consolidated_schedules = consolidate_schedules(existing_schedules + [new_schedule])

    # Publish only the consolidated schedules
    iot.publish(
        topic=MQTT_TOPIC,
        qos=1,
        payload=json.dumps({'schedules': consolidated_schedules})
    )

    return {
        'statusCode': 200,
        'body': json.dumps({'success': True, 'message': 'Schedule updated successfully'})
    }

# Function to clear all schedules
def clear_schedules():
    try:
        response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix='feeding-schedules/')
        if 'Contents' in response:
            for obj in response['Contents']:
                s3.delete_object(Bucket=BUCKET_NAME, Key=obj['Key'])

            # Publish empty schedules to the MQTT topic
            iot.publish(
                topic=MQTT_TOPIC,
                qos=1,
                payload=json.dumps({'schedules': []})
            )

            return {
                'statusCode': 200,
                'body': json.dumps({'success': True, 'message': 'All schedules cleared'})
            }
        else:
            return {
                'statusCode': 200,
                'body': json.dumps({'success': True, 'message': 'No schedules to clear'})
            }
    except Exception as e:
        print(f"Error clearing schedules: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Failed to clear schedules'})
        }

# Helper function to get existing schedules from S3
def get_existing_schedules():
    try:
        response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix='feeding-schedules/')
        schedules = []

        if 'Contents' in response:
            for obj in response['Contents']:
                obj_data = s3.get_object(Bucket=BUCKET_NAME, Key=obj['Key'])
                schedule = json.loads(obj_data['Body'].read().decode('utf-8'))
                schedules.append(schedule)

        return schedules

    except Exception as e:
        print(f"Error fetching existing schedules: {e}")
        return []

# Helper function to consolidate schedules
def consolidate_schedules(schedules):
    consolidated = {}

    for schedule in schedules:
        time = schedule['time']
        if time in consolidated:
            # Combine days and ensure uniqueness
            consolidated[time] = list(set(consolidated[time] + schedule['days']))
        else:
            consolidated[time] = schedule['days']

    # Format the consolidated schedules as a list
    return [{'id': str(int(datetime.now().timestamp() * 1000)), 'time': time, 'days': days} for time, days in consolidated.items()]
