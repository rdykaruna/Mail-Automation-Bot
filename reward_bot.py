import os
import time
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from gmail_test import authenticate_gmail 

def already_run_today(task_name):
    """Checks a file to see if we already triggered this task today."""
    filename = f"{task_name}_last_run.txt"
    today = datetime.now().strftime('%Y-%m-%d')
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            if f.read().strip() == today:
                return True
    return False

def mark_as_done(task_name):
    """Saves today's date so we don't run this task again."""
    filename = f"{task_name}_last_run.txt"
    today = datetime.now().strftime('%Y-%m-%d')
    with open(filename, 'w') as f:
        f.write(today)

def create_alarm(calendar, title, delay_minutes=4, specific_hour=None):
    """Creates the Google Calendar event starting 4 minutes from now."""
    now = datetime.now()
    if specific_hour is not None:
        # For the fixed 8:00 PM alert
        alarm_time = now.replace(hour=specific_hour, minute=0, second=0, microsecond=0)
        if alarm_time < now:
            alarm_time += timedelta(days=1)
    else:
        # Set for exactly 4 minutes from the moment of detection
        alarm_time = now + timedelta(minutes=delay_minutes)

    event = {
        'summary': title,
        'start': {'dateTime': alarm_time.isoformat(), 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': (alarm_time + timedelta(minutes=15)).isoformat(), 'timeZone': 'Asia/Kolkata'},
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': 0}, # Trigger at the exact start time
            ],
        },
    }
    calendar.events().insert(calendarId='primary', body=event).execute()
    print(f"⏰ Alarm Syncing: {title} scheduled for {alarm_time.strftime('%H:%M:%S')}")

def main():
    try:
        creds = authenticate_gmail()
        gmail_service = build('gmail', 'v1', credentials=creds)
        calendar_service = build('calendar', 'v3', credentials=creds)

        print("🚀 Bot is active. Keeping watch for BOTH Reward and Slot emails...")

        while True:
            try:
                # Check for unread messages
                results = gmail_service.users().messages().list(userId='me', q='is:unread').execute()
                messages = results.get('messages', [])

                for msg in messages:
                    m = gmail_service.users().messages().get(userId='me', id=msg['id']).execute()
                    snippet = m['snippet'].lower()
                    
                    # Task 1: Reward Points
                    if "assessment registration" in snippet or "reward points" in snippet:
                        if not already_run_today("reward"):
                            print("✅ Found Reward Mail!")
                            create_alarm(calendar_service, "REGISTER REWARD POINTS", 4)
                            create_alarm(calendar_service, "TEST TONIGHT 8PM", 0, specific_hour=20)
                            mark_as_done("reward")
                        else:
                            print("⏭️ Reward alert already done today.")

                    # Task 2: Slot Booking
                    elif "assessment booking" in snippet or "portal" in snippet:
                        if not already_run_today("slot"):
                            print("✅ Found Slot Booking Mail!")
                            create_alarm(calendar_service, "BOOK PORTAL SLOT NOW", 4)
                            mark_as_done("slot")
                        else:
                            print("⏭️ Slot alert already done today.")

                    # Mark as read
                    gmail_service.users().messages().batchModify(
                        userId='me', 
                        body={'removeLabelIds': ['UNREAD'], 'ids': [msg['id']]}
                    ).execute()

                time.sleep(30) # Check every 30 seconds
                
            except Exception as e:
                print(f"⚠️ Connection error: {e}. Retrying in 60s...")
                time.sleep(60)
                
    except KeyboardInterrupt:
        print("\nStopping safely...")

if __name__ == '__main__':
    main()