# PagerDuty Schedule Import & Export

This project provides scripts to help you manage PagerDuty schedules and users in bulk using CSV files.

## Features
- **Bulk Add Users to Schedules:** Use a CSV file to add users to PagerDuty schedules in the order you specify.
- **Export Schedules:** Export all on-call shifts for all schedules to a single master CSV file, with user names and dates.

## Prerequisites
- Python 3.8+
- A PagerDuty API key (with appropriate permissions)
- The following Python packages:
  - `pagerduty-api`
  - `python-dotenv`

Install dependencies with:
```
pip install pagerduty-api python-dotenv
```

## Setup
1. **Clone this repository** and open it in VS Code.
2. **Create a `.env` file** in the project root with your PagerDuty API key:
   ```
   PD_API_KEY=your_pagerduty_api_key_here
   ```
3. **Prepare your input CSV** (e.g., `TLT_Schedule.csv`) with the following columns:
   ```csv
   UserID,ScheduleID
   PAGERDUTY_USERID,PAGERDUTY_SCHEDULEID
   ...
   ```
   - You can get user and schedule IDs using the provided `GetAllUsers.py` and `GetAllSchedules.py` scripts.

## Usage

### 1. Add Users to Schedules
Run the script to add users to schedules in the order specified in your CSV:
```
python AppendToSchedule.py
```
- The script will read your CSV, add users to the specified schedules, and print progress.
- Each user will be added to the first layer of the schedule, in the order they appear in the CSV.

### 2. Export All Schedules to a Master CSV
Run the script to export all on-call shifts for all schedules:
```
python GetAllSchedules.py
```
- The script will create a `Final-Schedules/Master_Schedule.csv` file with columns:
  - `Schedule Name`, `User Name`, `Start Date`
- The export covers all shifts up to the last day of September of the current year.

### 3. Get All Users or Schedules
- To get a list of all users:
  ```
  python GetAllUsers.py
  ```
- To get a list of all schedules:
  ```
  python GetAllSchedules.py
  ```

## Notes
- Make sure your `.env` file is present and correct before running any scripts.
- The scripts will create output files in the `Final-Schedules` directory.
- If you encounter encoding issues with CSVs, ensure they are saved as UTF-8 (with or without BOM).
- It is easier to wipe out all people on a schedule from Pager Duty and reimport them all
- I haven't changed this to run every file in the import-files folder at once, you need to change the input file in AppendToSchedule.py, once we are confident it works then we can change this. 
- Most changes for August and September should now just be done in Pager Duty using 'overrides'
- Details of the users Pager Duty ID is in the rota spreadsheet
- To get the import files I have just been doing a vlookup of the id from the name. It's a bit manual, but fine for now (see the SoftwareEng schedule tab in the rota excel sheet as an example).
- There are some quirks with schedules, the schedule as a 'start date' which is before our rota starts. This 'start date' is where the list of users starts rotating from. So what you might find is you need to pad the start of the rota out with around 6 days worth of people to bring the rota to the correct start date. i.e. the schedule starts on the 28th July, we formally start on the 4th August, so you need to pad the days between the 28th and 4th. If you don't do this, the ordering of people will be 6 days out.

## License
MIT
