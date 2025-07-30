import boto3
import json
from datetime import datetime, timezone, timedelta

s3 = boto3.client('s3')
sns = boto3.client('sns')
BUCKET_NAME = 'fish-feeder-logs'
PST = timezone(timedelta(hours=-8))  # Pacific Standard Time

def lambda_handler(event, context):
    try:
        # Log the event for debugging
        print(f"Event received: {json.dumps(event)}")

        # Parse the log entry directly from the event
        log_entry = event  # IoT rule passes the payload directly

        # Get current time in UTC and convert to PST
        utc_now = datetime.now(timezone.utc)
        pst_now = utc_now.astimezone(PST)
        formatted_time = pst_now.strftime('%Y-%m-%d %H:%M:%S')

        # Update log entry with formatted PST time
        log_entry['time'] = formatted_time

        # Save the log to S3
        key = f"feeding-logs/{log_entry['id']}.json"
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=key,
            Body=json.dumps(log_entry),
            ContentType='application/json'
        )

        # Determine the notification message
        if log_entry['method'] == 'manual':
            message = f"Feeding triggered manually at {log_entry['time']}."
        else:
            message = f"Feeding triggered by schedule at {log_entry['time']}."

        # Send SNS notification
        sns.publish(
            Message=message,
            Subject="Feeding Notification",
            TopicArn="arn:aws:sns:<region>:<account-id>:FeedingNotifications"  # Replace with actual SNS ARN
        )

        print(f"Feeding log saved and notification sent: {message}")
        return {'statusCode': 200, 'body': 'Log saved and notification sent.'}

    except Exception as e:
        print(f"Error processing feeding log: {e}")
        return {'statusCode': 50
