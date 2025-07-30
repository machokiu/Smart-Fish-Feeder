# Smart Fish Feeder

- It is a cloud-connected smart fish feeder using AWS IoT Core, Lambda, API Gateway, SNS, and S3 for automated and remote-controlled feeding.
- The system was built with a Raspberry Pi 3B, servo motor, and MQTT-based communication for real-time feeding commands and scheduling.
- Developed a secure WebUI (HTML, CSS, JavaScript) hosted on AWS S3, enabling users to set feeding schedules, trigger manual feedings, and receive email notifications of feeding activities.
- Leveraged Python for device-side control and AWS Lambda functions for serverless backend processing, ensuring scalable and reliable cloud integration.

# Key tools and technologies
- AWS IoT Core
- AWS Lambda
- API Gateway
- AWS S3
- AWS SNS
- Raspberry Pi
- Python
- JavaScript
- HTML/CSS

# Disclaimer

This repository showcases a project I developed for automating a fish feeding system using an IoT device (Raspberry Pi) integrated with AWS IoT. The project allows the user to trigger feedings either manually or based on a schedule, and log the actions via MQTT to AWS IoT.

### Important Note:
- **Credentials Removed:** All AWS credentials, endpoints, and sensitive configurations have been removed from the code for security purposes. These are required to run the project in a real environment. Without these credentials, the code will not work as intended.
  
- **Not Deployed on AWS Anymore:** This project was initially deployed to AWS IoT but is no longer running in that environment. The code is preserved here for reference and learning purposes, but it is no longer connected to any active AWS services.

- **Purpose of This Repository:** This repository serves as a record of my work on the project. Feel free to explore the code, which demonstrates how AWS IoT can be integrated with physical devices like a Raspberry Pi. If you wish to deploy this project on your own, you'll need to configure your AWS credentials and set up the necessary services yourself.
