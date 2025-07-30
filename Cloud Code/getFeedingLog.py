import boto3
import json

s3 = boto3.client('s3')
BUCKET_NAME = 'fish-feeder-logs'

def lambda_handler(event, context):
    try:
        # List all objects in the "feeding-logs/" folder
        response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix='feeding-logs/')

        # Check if the folder is empty
        if 'Contents' not in response:
            print("No log files found in S3.")
            return {
                'statusCode': 200,
                'body': json.dumps({'success': True, 'logItems': []})  # Return empty list if no files
            }

        logs = []

        # Iterate over the files in the "feeding-logs/" folder
        for obj in response['Contents']:
            # Fetch each log file from S3
            obj_data = s3.get_object(Bucket=BUCKET_NAME, Key=obj['Key'])
            file_content = obj_data['Body'].read().decode('utf-8').strip()

            # Check if the file is empty
            if not file_content:
                print(f"Warning: File {obj['Key']} is empty.")
                continue  # Skip empty files

            # Try to parse the JSON content
            try:
                log_entry = json.loads(file_content)
                logs.append(log_entry)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON in file {obj['Key']}: {e}")
                continue  # Skip files that are not valid JSON

        # Sort logs by time (descending order, latest log first)
        logs.sort(key=lambda x: x['time'], reverse=True)

        # Limit to the 3 most recent logs
        recent_logs = logs[:3]

        return {
            'statusCode': 200,
            'body': json.dumps({'success': True, 'logItems': recent_logs})
        }

    except Exception as e:
        print(f"Error fetching feeding logs: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal Server Error'})
        }
