import boto3
import json
from datetime import datetime, timezone, timedelta

s3 = boto3.client('s3')
iot = boto3.client('iot-data', region_name='us-west-2')
BUCKET_NAME = 'fish-feeder-logs'


# Define the PST timezone offset (UTC - 8 hours)
PST = timezone(timedelta(hours=-8))

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        action = body.get('action')
        time = body.get('time')

        if not action or not time:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Action and time are required'})
            }

        # Get current time in UTC, then convert to PST
        utc_now = datetime.now(timezone.utc)  # Get current time in UTC
        pst_now = utc_now.astimezone(PST)  # Convert to PST
        formatted_time = pst_now.strftime('%Y-%m-%d %H:%M:%S')  # Format the time for readability

        # Publish to IoT Core
        iot.publish(
            topic='iot/commands/feed-now',
            qos=1,
            payload=json.dumps({'action': 'feedNow', 'time': formatted_time})
        )

        return {
            'statusCode': 200,
            'body': json.dumps({'success': True, 'message': 'Feeding triggered successfully'})
        }

    except Exception as e:
        print(f"Error triggering feeding: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal Server Error'})
        }
