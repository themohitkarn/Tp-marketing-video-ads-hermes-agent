import os
from dotenv import load_dotenv
from apify_client import ApifyClient

load_dotenv()

api_token = os.getenv("APIFY_API_TOKEN")

if not api_token:
    raise ValueError("APIFY_API_TOKEN not found in .env file")

client = ApifyClient(api_token)

user = client.user().get()

print("\nAPIFY CONNECTION SUCCESSFUL!\n")

print("Username:", user.username)
print("Email:", user.email)