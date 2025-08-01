import os
import csv
import datetime
from pagerduty.rest_api_v2_client import RestApiV2Client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

PD_API_KEY = os.environ.get("PD_API_KEY")
if not PD_API_KEY:
    raise ValueError("PD_API_KEY environment variable not set.")

pd = RestApiV2Client(api_key=PD_API_KEY)

def get_schedule_on_calls(schedule_id, start_date, end_date):
    """Fetches on-call users for a given schedule and time range."""
    params = {
        'schedule_ids[]': [schedule_id],
        'since': start_date.isoformat(),
        'until': end_date.isoformat()
    }
    # Use iter_all to handle pagination for the /oncalls endpoint
    return pd.iter_all('/oncalls', params=params)

def export_master_schedule_to_csv(all_on_calls):
    """Exports a list of all on-call shifts to a single master CSV file."""
    # Create the directory if it doesn't exist
    output_dir = "Final-Schedules"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    csv_filename = os.path.join(output_dir, "Master_Schedule.csv")
    print(f"\nExporting all shifts to '{csv_filename}'...")

    if not all_on_calls:
        print("No on-call shifts found to export.")
        return

    try:
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Schedule Name', 'User Name', 'Start Date'])
            
            for on_call in all_on_calls:
                # Parse the start time and format it to a short date
                start_datetime = datetime.datetime.fromisoformat(on_call['start'].replace('Z', '+00:00'))
                short_date = start_datetime.strftime('%Y-%m-%d')
                
                writer.writerow([
                    on_call['schedule_name'],
                    on_call['user']['summary'],
                    short_date
                ])
        
        print(f"Successfully exported {len(all_on_calls)} total on-call shifts to '{csv_filename}'")

    except Exception as e:
        print(f"Error exporting master schedule to CSV: {e}")

def get_all_schedules():
    """Gets all schedules from PagerDuty."""
    print("Fetching all schedules...")
    try:
        return pd.list_all('/schedules')
    except Exception as e:
        print(f"Failed to fetch schedules: {e}")
        return []

if __name__ == "__main__":
    all_schedules = get_all_schedules()
    master_on_call_list = []

    if all_schedules:
        print(f"Found {len(all_schedules)} schedules to process.")
        
        # Define the time range for the export
        start_date = datetime.datetime.now()
        # Set end date to the last day of September of the current year
        end_date = datetime.datetime(start_date.year, 9, 30, 23, 59, 59)

        for schedule in all_schedules:
            schedule_id = schedule['id']
            schedule_name = schedule['name']
            print(f"Processing schedule: {schedule_name} (ID: {schedule_id})")
            
            try:
                on_calls = get_schedule_on_calls(schedule_id, start_date, end_date)
                
                # Add schedule name to each on-call entry and append to master list
                for on_call in on_calls:
                    on_call['schedule_name'] = schedule_name
                    master_on_call_list.append(on_call)
            except Exception as e:
                print(f"Could not process schedule {schedule_name}: {e}")
        
        export_master_schedule_to_csv(master_on_call_list)
        print("\nAll schedules processed.")
    else:
        print("No schedules found or an error occurred.")
