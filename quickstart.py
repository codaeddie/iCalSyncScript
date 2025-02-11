import datetime
import os.path
import requests

from icalendar import Calendar
from datetime import datetime
from datetime import timezone
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

def fetch_and_parse_ical(url):
    """Fetches iCal data from URL and returns parsed events"""
    response = requests.get(url)
    response.raise_for_status()  # Raises exception for 4XX/5XX errors
    
    cal = Calendar.from_ical(response.text)
    events = []
    
    for component in cal.walk('VEVENT'):
        event = {
            'summary': str(component.get('summary')),
            'start': {
                'dateTime': component.get('dtstart').dt.astimezone(timezone.utc).isoformat(),
                'timeZone': 'UTC'
            },
            'end': {
                'dateTime': component.get('dtend').dt.astimezone(timezone.utc).isoformat(),
                'timeZone': 'UTC'
            }
        }
        events.append(event)
    return events


def main():
  """Shows basic usage of the Google Calendar API.
  Prints the start and name of the next 10 events on the user's calendar.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
        service = build("calendar", "v3", credentials=creds)
        
        # Get the Apple Calendar URL from user
        apple_url = input("Enter the Apple Calendar URL: ")
        
        # Fetch and parse events
        print("Fetching events from Apple Calendar...")
        events = fetch_and_parse_ical(apple_url)
        
        print(f"Found {len(events)} events. Creating them in your primary calendar...")
        
        # Create each event in Google Calendar
        for event in events:
            result = service.events().insert(
                calendarId='primary',
                body=event
            ).execute()
            print(f"Created event: {result.get('summary')}")
        
        print("Done! All events have been added to your primary calendar.")

  except HttpError as error:
        print(f"An error occurred: {error}")
  except requests.exceptions.RequestException as error:
        print(f"Failed to fetch Apple Calendar: {error}")


if __name__ == "__main__":
  main()