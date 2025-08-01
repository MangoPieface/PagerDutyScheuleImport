import os
from pagerduty.rest_api_v2_client import RestApiV2Client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

PD_API_KEY = os.environ.get("PD_API_KEY")

pd = RestApiV2Client(api_key=PD_API_KEY)

def get_all_users():
    users = []
    for user in pd.iter_all('/users'):
        users.append(user)
    return users

if __name__ == "__main__":
    all_users = get_all_users()
    for user in all_users:
        print(f'"{user["name"]}","{user["id"]}","{user["email"]}",')
