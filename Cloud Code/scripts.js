// Base URL for API Gateway
const API_BASE_URL = 'https://vfuww6i7na.execute-api.us-west-2.amazonaws.com/v2';


// Utility function to make API requests
const makeApiRequest = async (endpoint, method = 'GET', data = null) => {
    const headers = {
        'Content-Type': 'application/json',
    };

    const options = {
        method: method,
        headers: headers,
    };

    if (data) {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(API_BASE_URL + endpoint, options);
        return response.json();
    } catch (error) {
        console.error('Error making API request:', error);
        alert('Failed to connect to the server. Please try again.');
    }
};

// Trigger Feeding Action (Manual feed)
const feedNow = async () => {
    const data = {
        action: 'manual',
        time: new Date().toISOString(),
    };

    const response = await makeApiRequest('/feed-now', 'POST', data);

    if (response.success) {
        alert('Feeding triggered!');
        refreshFeedingLog();
    } else {
        alert('Error triggering feeding!');
    }
};

// Add or update feeding schedule
const addOrUpdateSchedule = async () => {
    const time = document.getElementById('schedule-time').value;
    const days = [];
    document.querySelectorAll('input[name="days"]:checked').forEach((checkbox) => {
        days.push(checkbox.value);
    });

    if (!time || days.length === 0) {
        alert('Please select a time and at least one day.');
        return;
    }

    const scheduleData = {
        action: 'update',  // Added action field for update
        time: time,
        days: days,
    };

    const response = await makeApiRequest('/update-schedule', 'POST', scheduleData);

    if (response.success) {
        alert('Schedule updated!');
        refreshSchedule();
    } else {
        alert('Error updating schedule: ' + (response.error || response.message));
    }
};

// Clear all feeding schedules
const clearAllSchedules = async () => {
    
    const response = await makeApiRequest('/clear-schedule', 'POST', { action: 'clear' }); 

    if (response.success) {
        alert('All schedules cleared!');
        refreshSchedule();  // Refresh the schedule display
    } else {
        alert('Error clearing schedules!');
    }
};



// Refresh and display the feeding log
const refreshFeedingLog = async () => {
    const response = await makeApiRequest('/get-feeding-log', 'GET');

    if (response.success) {
        const logItems = response.logItems;
        const logContainer = document.getElementById('feeding-log-items');
        logContainer.innerHTML = '';  // Clear current log display

        // Populate log items
        logItems.forEach(item => {
            const logEntry = document.createElement('li');
            logEntry.textContent = `Time: ${item.time} | Method: ${item.method}`;
            logContainer.appendChild(logEntry);
        });
    }
};

// Refresh and display the feeding schedule
const refreshSchedule = async () => {
    const response = await makeApiRequest('/get-schedule', 'GET');

    if (response.success) {
        const scheduleItems = response.scheduleItems;
        const scheduleContainer = document.getElementById('schedule-list-items');
        scheduleContainer.innerHTML = '';  // Clear current schedule display

        // Populate consolidated schedules
        scheduleItems.forEach(item => {
            const scheduleEntry = document.createElement('li');
            scheduleEntry.textContent = `Time: ${item.time} | Days: ${item.days.join(', ')}`;
            scheduleContainer.appendChild(scheduleEntry);
        });
    } else {
        alert('Failed to load schedule.');
    }
};


// Set event listeners for buttons
document.getElementById('feed-now').addEventListener('click', feedNow);
document.getElementById('add-schedule').addEventListener('click', addOrUpdateSchedule);
document.getElementById('clear-schedule').addEventListener('click', clearAllSchedules);

// Call refresh functions when the page loads
window.onload = () => {
    refreshFeedingLog();  // Load feeding logs
    refreshSchedule();    // Load current feeding schedules
};