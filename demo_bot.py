import time
import base64
import re
from datetime import datetime
from googleapiclient.discovery import build
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from gmail_test import authenticate_gmail

def get_link_from_gmail(service, start_time):
    """Searches only for NEW unread emails sent after the script started."""
    # Convert start_time to a Unix timestamp for the Gmail query
    # 'after:' uses seconds, so we filter strictly for new arrivals
    query = f'is:unread "Assessment Registration" after:{start_time}'
    
    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages', [])

    if not messages:
        return None

    msg = service.users().messages().get(userId='me', id=messages[0]['id']).execute()
    payload = msg['payload']
    
    # Extract HTML body
    parts = payload.get('parts', [])
    data = ""
    if parts:
        for part in parts:
            if part['mimeType'] == 'text/html':
                data = part['body']['data']
    else:
        data = payload['body']['data']

    html_content = base64.urlsafe_b64decode(data).decode()
    links = re.findall(r'href=[\'"]?([^\'" >]+)', html_content)
    
    if links:
        # Mark as read immediately to prevent loops
        service.users().messages().batchModify(
            userId='me', 
            body={'removeLabelIds': ['UNREAD'], 'ids': [messages[0]['id']]}
        ).execute()
        return links[0]
    return None

def run_automation(target_url):
    print(f"🚀 NEW MAIL DETECTED! Opening: {target_url}")
    edge_options = Options()
    edge_options.add_experimental_option("detach", True)
    driver = webdriver.Edge(options=edge_options)
    
    try:
        driver.get(target_url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "name")))
        
        # Filling your details
        fields = [
            ("name", "Karunakaran M"),
            ("email", "karunakaranm.ug.24.ad@francisxavier.ac.in"),
            ("dept", "AI & Data Science")
        ]
        
        for field_id, value in fields:
            time.sleep(1)
            driver.find_element(By.ID, field_id).send_keys(value)
            
        time.sleep(1)
        driver.find_element(By.ID, "register_btn").click()
        print("🎉 SUCCESS: Registration on Live Portal Complete!")
        
    except Exception as e:
        print(f"❌ Automation Error: {e}")

def main():
    creds = authenticate_gmail()
    service = build('gmail', 'v1', credentials=creds)
    
    # Capture the exact time the script starts (Unix timestamp)
    start_timestamp = int(datetime.now().timestamp())
    
    print(f"🚀 Bot Active. Waiting for 'Assessment Registration' mail...")
    
    while True:
        target_url = get_link_from_gmail(service, start_timestamp)
        
        if target_url:
            run_automation(target_url)
            # Update start_timestamp to current time so it doesn't re-process
            start_timestamp = int(datetime.now().timestamp())
            print("\n✅ Registration finished. Ready for the next one...")
        else:
            time.sleep(5) 

if __name__ == "__main__":
    main()