# Cloud Configuration

This document provides the configuration steps for setting up the **Smart Fish Feeder system**, including **AWS Cloud Services**, **IoT Core**, and the **Web UI** hosted on S3.  
This setup enables automated and manual fish feeding with real-time logging and notifications.

---

## 1️⃣ API Gateway Setup

1. Create an **API Gateway** instance.
2. Set up API routes for each function:
   - `/feed-now` → Trigger manual feeding.
   - `/update-schedule` → Update feeding schedules.
   - `/get-schedule` → Fetch existing feeding schedules.
   - `/clear-schedule` → Clear all feeding schedules.
   - `/get-feeding-log` → Fetch the latest feeding logs.
3. Link each route to its **corresponding Lambda function**.

---

## 2️⃣ Lambda Functions Setup

### FeedingTrigger
- Triggered by manual feeding requests from the Web UI.
- Publishes a message to the `iot/commands/feed-now` topic to instruct the Raspberry Pi to feed the fish.

### FeedingScheduleUpdate
- Updates the feeding schedule in **S3**.
- Checks for **duplicate schedules** before adding a new one.
- Publishes the updated schedule to `iot/commands/update-schedule`.
- Combines the new schedule with existing ones for **consistent updates**.

### FeedingLog
- Triggered when the Raspberry Pi publishes a feeding event to `iot/commands/feed-log`.
- Stores the feeding log in **S3**.
- Sends **email notifications** for each feeding event using **SNS**.

### getFeedingSchedule
- Fetches all existing feeding schedules from S3.
- Returns the data to display schedules on the Web UI.

### getFeedingLog
- Retrieves the latest feeding logs from S3.
- Returns the most recent logs to the Web UI for display.

---

## 3️⃣ IoT Core Setup

1. Create **IoT Things** for physical devices (e.g., Raspberry Pi).
2. Define **MQTT topics** for communication:
   - `iot/commands/feed-now` → Manual feeding requests.
   - `iot/commands/update-schedule` → Feeding schedule updates.
   - `iot/commands/feed-log` → Feeding log messages from Raspberry Pi.
3. Set up **IoT policies and permissions**:
   - Allow **Lambda functions** to publish to topics.
   - Allow **devices** to subscribe to topics.
4. Create an **IoT Rule** to trigger the `FeedingLog` Lambda function on messages from `iot/commands/feed-log`.

---

## 4️⃣ SNS Setup

1. Create an **SNS topic** named `FeedingNotification`.
2. Subscribe user **emails** to this SNS topic.
3. Configure **Lambda functions** to publish feeding notifications to this topic.

---

## 5️⃣ S3 Setup

1. Create an **S3 bucket** named `fish-feeder-logs`.
2. Create folders:
   - `feeding-logs/` → Stores feeding log files.
   - `feeding-schedules/` → Stores feeding schedules.
3. Attach IAM policies to Lambda functions to allow `s3:GetObject` and `s3:PutObject` actions.

---

## 6️⃣ Web Interface Configuration

### Web UI Setup
1. Build a **Dashboard page** with HTML and CSS to:
   - Trigger **manual feeding**.
   - Manage feeding schedules.
   - View feeding logs.
2. Use **JavaScript** to call API routes:
   - `/feed-now`
   - `/update-schedule`
   - `/get-schedule`
   - `/clear-schedule`
   - `/get-feeding-log`
3. Deploy the Web UI to **Amazon S3** for static website hosting
