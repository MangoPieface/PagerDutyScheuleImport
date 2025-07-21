import os
import csv
import datetime
from pagerduty import PagerDuty

PD_API_KEY = os.environ.get("PD_API_KEY")
PD_SUBDOMAIN = "your_subdomain"
pd = PagerDuty(PD_SUBDOMAIN, api_token=PD_API_KEY)

# Map display names to PagerDuty user IDs
USER_NAME_TO_ID = {
    "Name from Rota 1": "PagerDuty User ID",
     "Name from Rota 1": "PagerDuty User ID",
    # ... add all users
}

def parse_date(date_str):
    # Example: "Mon 04/Aug/2025"
    return datetime.datetime.strptime(date_str.strip(), "%a %d/%b/%Y").date()

def create_daily_schedule(date, user_ids):
    name = f"Rota {date.strftime('%Y-%m-%d')}"
    start = datetime.datetime.combine(date, datetime.time(8, 0))
    end = datetime.datetime.combine(date, datetime.time(21, 0))
    schedule = pd.schedules.create(
        name=name,
        time_zone="UTC",
        description=f"Daily rota for {date.strftime('%Y-%m-%d')}",
        schedule_layers=[{
            "name": "Day Layer",
            "start": start.isoformat(),
            "rotation_virtual_start": start.isoformat(),
            "rotation_turn_length_seconds": (end - start).seconds,
            "users": [{"user": {"id": uid, "type": "user_reference"}} for uid in user_ids],
            "restrictions": []
        }]
    )
    return schedule

def import_from_csv(csv_path):
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            date = parse_date(row['Date'])
            user_ids = [
                USER_NAME_TO_ID.get(row['Cloud Engineer 1'].strip()),
                USER_NAME_TO_ID.get(row['Cloud Engineer 2'].strip()),
                USER_NAME_TO_ID.get(row['Software Engineer'].strip()),
                USER_NAME_TO_ID.get(row['Product Manager'].strip()),
                USER_NAME_TO_ID.get(row['TLT'].strip()),
            ]
            if None in user_ids:
                print(f"Missing user mapping for {row}")
                continue
            create_daily_schedule(date, user_ids)
            print(f"Created schedule for {date} with users {user_ids}")

def clear_all_schedules():
    for schedule in pd.schedules.list():
        pd.schedules.delete(schedule['id'])
        print(f"Deleted schedule {schedule['name']}")

if __name__ == "__main__":
    # import_from_csv("rota.csv")
    # clear_all_schedules()
    pass