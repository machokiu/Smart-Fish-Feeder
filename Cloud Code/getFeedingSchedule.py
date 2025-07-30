import boto3
import json

s3 = boto3.client('s3')
BUCKET_NAME = 'fish-feeder-logs'

def lambda_handler(event, context):
    try:
        # List all objects in the "feeding-schedules/" folder
        response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix='feeding-schedules/')

        # Check if the folder is empty
        if 'Contents' not in response:
            print("No schedule files found in S3.")
            return {
                'statusCode': 200,
                'body': json.dumps({'success': True, 'scheduleItems': []})  # Return empty list if no files
            }

        schedules = []

        # Iterate over the files in the "feeding-schedules/" folder
        for obj in response['Contents']:
            # Fetch each schedule file from S3
            obj_data = s3.get_object(Bucket=BUCKET_NAME, Key=obj['Key'])
            file_content = obj_data['Body'].read().decode('utf-8').strip()

            # Check if the file is empty
            if not file_content:
                print(f"Warning: File {obj['Key']} is empty.")
                continue  # Skip empty files

            # Try to parse the JSON content
            try:
                schedule = json.loads(file_content)
                schedules.append(schedule)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON in file {obj['Key']}: {e}")
                continue  # Skip files that are not valid JSON

        # Consolidate schedules by time
        consolidated_schedules = consolidate_schedules(schedules)

        return {
            'statusCode': 200,
            'body': json.dumps({'success': True, 'scheduleItems': consolidated_schedules})
        }

    except Exception as e:
        print(f"Error fetching feeding schedules: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal Server Error'})
        }


# Helper function to consolidate schedules by time
def consolidate_schedules(schedules):
    consolidated = {}

    for schedule in schedules:
        time = schedule['time']
        if time in consolidated:
            consolidated[time] = list(set(consolidated[time] + schedule['days']))
        else:
            consolidated[time] = schedule['days']

    # Format consolidated schedules as a list
    return [{'time': time, 'days': days} for time, days in consolidated.items()]
