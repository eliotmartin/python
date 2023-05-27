#!/usr/bin/env python3
# ------------------------------------------------------------------------
# Log Remaing Time
# Calculate and log remaining time in Harvest
# ------------------------------------------------------------------------


# Generic/Built-in modules
import requests                                                 # Requests Library
import datetime                                                 # DateTime Library
import logging                                                  # Logging Library

# Define Variables
user_id = ""
account_id = ""
project_name = ""
task_name = ""
access_token = ""
base_url = f"https://api.harvestapp.com/v2/"
headers = {
    "Harvest-Account-ID": account_id,
    "Authorization": f"Bearer {access_token}",
    "User-Agent": "My Harvest API Client"
}

# Configure logging
logging.basicConfig(filename='time_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# function to Get Project ID
def get_project_id(project_name):
    url = f"{base_url}/projects"
    response = requests.get(url, headers=headers)
    projects = response.json()["projects"]
    for project in projects:
        if project["name"] == project_name:
            return project["id"]
    return None


#Function to Get Task ID
def get_task_id(task_name):
    url = f"{base_url}/tasks"
    response = requests.get(url, headers=headers)
    tasks = response.json()["tasks"]
    for task in tasks:
        if task["name"] == task_name:
            return task["id"]
    return None


# Function to Get Total Time Today
def get_total_time_logged(user_id):
    url = f"{base_url}/time_entries"
    today = datetime.date.today().isoformat()
    params = {
        "user_id": user_id,
        "from": today + "T00:00:00Z",
        "to": today + "T23:59:59Z",
        "is_running": "false",
        "is_billed": "false"
    }
    response = requests.get(url, headers=headers, params=params)
    time_entries = response.json()["time_entries"]
    total_time_logged = sum(entry["hours"] for entry in time_entries)
    return total_time_logged


# Function to Calculate Reaminin Time
def calculate_remaining_time(user_id):
    total_time_logged = get_total_time_logged(user_id)
    remaining_time_left = 7.5 - total_time_logged
    remaining_time_left = max(remaining_time_left, 0)  # Prevent negative values
    return remaining_time_left

# Function to Log Remaining Time
def create_time_entry(user_id, project_id, task_id, hours):
    url = f"{base_url}/time_entries"
    today = datetime.date.today().isoformat()
    data = {
        "user_id": user_id,
        "project_id": project_id,
        "task_id": task_id,
        "spent_date": today,
        "hours": hours
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        print("Time entry created successfully.")
    else:
        print("Failed to create time entry.")

# Main
def main():

    
    # Get the Total Time logged Today and Calculate the Ramining Time (Based on a 7.5 hour working Day)
    total_time_logged = get_total_time_logged(user_id)
    remaining_time = calculate_remaining_time(user_id)
    #print("API Response:", response.json())

    # Get the Project and Task ID
    project_id = get_project_id(project_name)
    task_id = get_task_id(task_name)

    # Log the Output
    current_date = datetime.date.today().strftime("%Y-%m-%d")
    logging.info("[%s] Current Total Time: %s hours", current_date, total_time_logged)
    logging.info("[%s] Remaining Time    : %s hours", current_date, remaining_time)

    if remaining_time > 0:
        if project_id and task_id:
            create_time_entry(user_id, project_id, task_id, remaining_time)
            logging.info("[%s] Time entry created successfully.", current_date)
        else:
            if not project_id:
                logging.error("[%s] Cannot log time. Project '%s' not found.", current_date, project_name)
            if not task_id:
                logging.error("[%s] Cannot log time. Task '%s' not found.", current_date, task_name)
    else:
        logging.info("[%s] Nothing to log. Remaining time is 0.", current_date)

    
if __name__ == "__main__":
    main()
