import os
import csv
from pagerduty.rest_api_v2_client import RestApiV2Client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
# Ensure your PagerDuty API key is set in a .env file or as an environment variable
PD_API_KEY = os.environ.get("PD_API_KEY")
if not PD_API_KEY:
    raise ValueError("PD_API_KEY environment variable not set. Please create a .env file or set it.")

# Initialize the PagerDuty client
pd = RestApiV2Client(api_key=PD_API_KEY)

def add_user_to_schedule(schedule_id, user_id):
    """
    Adds a user to the first layer of a given PagerDuty schedule.

    :param schedule_id: The ID of the schedule to update.
    :param user_id: The ID of the user to add.
    """
    try:
        # Fetch user details to get the name
        #print(f"Fetching user with ID: {user_id}...")
        user_response = pd.request("GET", f"/users/{user_id}")
        user_data = user_response.json()
        user_name = user_data.get('user', {}).get('name', f"Unknown User ID: {user_id}")

        #print(f"Fetching schedule with ID: {schedule_id}...")
        # Get the schedule details, including its layers
        schedule_response = pd.request("GET", f"/schedules/{schedule_id}", params={'include[]': 'schedule_layers'})
        schedule_data = schedule_response.json()
        schedule = schedule_data.get('schedule')

        if not schedule:
            print(f"Error: Schedule with ID '{schedule_id}' not found.")
            return

        schedule_name = schedule.get('name', f"Unknown Schedule ID: {schedule_id}")

        if not schedule.get('schedule_layers'):
            print(f"Error: No schedule layers found for schedule '{schedule_name}' (ID: {schedule_id}). Cannot add users.")
            return
        #print(f"schedule '{schedule_name}'.")
        # Add the user to the first layer
        # In a more complex scenario, you might need logic to select the correct layer
        layer = schedule['schedule_layers'][0]
        
        new_user_entry = {'user': {'id': user_id, 'type': 'user_reference'}}

        #print(f"Adding user '{user_name}' to schedule '{schedule_name}'...")
        layer.setdefault('users', []).append(new_user_entry)

        # Update the schedule with the modified layer
        update_payload = {'schedule': schedule}
        pd.request("PUT", f"/schedules/{schedule_id}", json=update_payload)
        
        print(f"{user_name}")

    except Exception as e:
        print(f"An error occurred while processing schedule {schedule_id} for user {user_id}: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"API Error ({e.response.status_code}): {e.response.text}")


def import_users_to_schedules_from_csv(csv_path):
    """
    Reads a CSV file with ScheduleID and UserID columns and adds each user
    to the specified schedule.
    """
    try:
        with open(csv_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                schedule_id = row.get('ScheduleID')
                user_id = row.get('UserID')
                if schedule_id and user_id:
                    add_user_to_schedule(schedule_id.strip(), user_id.strip())
                else:
                    print(f"Skipping invalid row: {row}")
    except FileNotFoundError:
        print(f"Error: The file '{csv_path}' was not found.")
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")

if __name__ == "__main__":
    # The CSV file should have two columns: UserID and ScheduleID
    csv_file_path = 'Import-files/SoftwareEngineering_Schedule.csv'
    import_users_to_schedules_from_csv(csv_file_path)