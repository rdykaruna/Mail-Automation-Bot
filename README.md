# Mail Automation Suite

A collection of automated bots for Gmail monitoring, Google Calendar alerts, and web automation for assessment registration workflows.

## What This Project Does

This suite includes three automation bots designed to streamline assessment registration and notification workflows:

### 1. **Reward Bot** ([reward_bot.py](reward_bot.py))
Monitors Gmail for assessment-related emails and creates automated calendar reminders:
- Watches unread messages every 30 seconds
- Detects emails containing "assessment registration" or "reward points"
- Creates two calendar alerts:
  - Immediate alert (4 minutes from detection)
  - Fixed evening alert (8:00 PM)
- Prevents duplicate alerts using daily tracking files
- Marks processed emails as read automatically

### 2. **Demo Bot** ([demo_bot.py](demo_bot.py))
Fully automated registration bot using Selenium WebDriver:
- Monitors Gmail for new "Assessment Registration" emails
- Extracts registration links from email content
- Automatically opens the link in Microsoft Edge
- Fills out registration form with pre-configured details
- Submits registration and keeps browser open for verification
- Only processes emails received after script startup

### 3. **Flask Test Server** ([app.py](app.py))
Local web server for testing the registration workflow:
- Simulates the assessment registration portal
- Features a clean, responsive UI styled like a real portal
- Accepts student details (name, email, department)
- Provides confirmation page after submission
- Perfect for testing without hitting production endpoints

## File Structure

```
├── reward_bot.py          # Calendar alert automation
├── demo_bot.py            # Selenium-based auto-registration
├── gmail_test.py          # OAuth authentication module
├── app.py                 # Flask test server
├── credentials.json       # Google OAuth client secrets (user-provided)
├── token.json             # Generated OAuth token cache
├── requirements.txt       # Python dependencies
├── reward_last_run.txt    # Tracks reward alert execution
├── slot_last_run.txt      # Tracks slot alert execution
└── mailenv/               # Python virtual environment
```

### Key Files Explained
- [gmail_test.py](gmail_test.py): Handles OAuth2 flow and token refresh for Gmail and Calendar APIs
- [reward_bot.py](reward_bot.py): Main monitoring loop for creating calendar reminders
- [demo_bot.py](demo_bot.py): Automated browser-based form submission
- [app.py](app.py): Local Flask server mimicking registration portal
- `credentials.json`: Google Cloud OAuth client secrets (must be obtained from Google Cloud Console)
- `token.json`: Auto-generated after first authentication
- `*_last_run.txt`: Daily tracking files to prevent duplicate executions

## Prerequisites

- **Python 3.10+** recommended
- **Microsoft Edge** browser (for demo_bot.py)
- **Google Cloud Project** with:
  - Gmail API enabled
  - Google Calendar API enabled
  - OAuth 2.0 Client ID (Desktop application type)
- OAuth credentials file saved as `credentials.json`

## Installation & Setup

### 1. Create Virtual Environment

```powershell
python -m venv mailenv
mailenv\Scripts\Activate.ps1
```

### 2. Install Dependencies

```powershell
pip install -r requirements.txt
```

Or install individually:
```powershell
pip install selenium flask requests google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### 3. Configure Google Cloud

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable **Gmail API** and **Google Calendar API**
4. Create OAuth 2.0 Client ID (Desktop application)
5. Download credentials and save as `credentials.json` in project root

### 4. First-Time Authentication

Run any bot for the first time:
```powershell
python gmail_test.py
```
- Browser will open for OAuth authorization
- Grant permissions for Gmail and Calendar access
- `token.json` will be created automatically
- You only need to do this once

## Usage

### Running the Reward Bot

```powershell
python reward_bot.py
```
- Monitors Gmail continuously
- Creates calendar alerts when trigger emails arrive
- Press `Ctrl+C` to stop gracefully
- Logs all actions to console

**Trigger phrases:**
- "assessment registration"
- "reward points"
- "assessment booking"
- "portal"

### Running the Demo Bot

```powershell
python demo_bot.py
```
- Waits for emails with "Assessment Registration"
- Automatically extracts and opens registration links
- Auto-fills form with configured details
- Keeps browser open after successful registration
- Press `Ctrl+C` to stop

**Note:** Update personal details in [demo_bot.py](demo_bot.py#L61-L64):
```python
fields = [
    ("name", "Your Name"),
    ("email", "your.email@college.edu"),
    ("dept", "Your Department")
]
```

### Running the Test Server

```powershell
python app.py
```
- Starts Flask server on `http://127.0.0.1:5000/`
- Navigate to the URL in your browser
- Test form submission locally
- Use this to test demo_bot without live portals

## Customization

### Changing Calendar Alert Times

Edit [reward_bot.py](reward_bot.py#L24):
```python
create_alarm(calendar_service, "REGISTER REWARD POINTS", 4)  # 4 minutes from now
create_alarm(calendar_service, "TEST TONIGHT 8PM", 0, specific_hour=20)  # 8 PM
```

### Modifying Search Phrases

Edit detection logic in [reward_bot.py](reward_bot.py#L67-L69):
```python
if "your custom phrase" in snippet:
    # Add your custom alert logic
```

### Adjusting Polling Interval

Edit sleep duration in [reward_bot.py](reward_bot.py#L93):
```python
time.sleep(30)  # Check every 30 seconds
```

Or in [demo_bot.py](demo_bot.py#L93):
```python
time.sleep(5)  # Check every 5 seconds
```

### Browser Settings (Demo Bot)

Modify Edge options in [demo_bot.py](demo_bot.py#L50):
```python
edge_options = Options()
edge_options.add_experimental_option("detach", True)  # Keep browser open
# edge_options.add_argument("--headless")  # Uncomment for headless mode
```

## Troubleshooting

### Authentication Issues
- Delete `token.json` and re-authenticate
- Verify `credentials.json` is valid
- Check that both APIs are enabled in Google Cloud Console
- Ensure OAuth consent screen is configured

### Demo Bot Not Working
- Verify Microsoft Edge is installed
- Check that Edge WebDriver matches your browser version
- Ensure the target website structure hasn't changed (update element IDs if needed)

### No Calendar Alerts
- Verify Google Calendar permissions were granted
- Check timezone settings in [reward_bot.py](reward_bot.py#L35) (currently `Asia/Kolkata`)
- Ensure calendar reminders are enabled in Google Calendar settings

### Bot Keeps Processing Same Email
- Check that emails are being marked as read
- Verify `*_last_run.txt` files are being created
- Delete tracking files to reset daily limits

## Security & Privacy

⚠️ **Important Security Notes:**
- `credentials.json` contains sensitive OAuth secrets
- `token.json` grants access to your Gmail and Calendar
- Never commit these files to version control
- Add to `.gitignore`:
  ```
  credentials.json
  token.json
  *_last_run.txt
  ```
- Rotate credentials if exposed
- Review OAuth permissions regularly in [Google Account Settings](https://myaccount.google.com/permissions)

## API Scopes Used

```python
SCOPES = [
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/calendar.events'
]
```

## License

This project is for educational and personal use. Ensure compliance with your institution's policies when automating registration processes.

## Contributing

To add new features:
1. Create feature-specific bot files
2. Use [gmail_test.py](gmail_test.py) for authentication
3. Follow existing patterns for email monitoring
4. Update this README with new bot documentation

## Support

For issues or questions:
- Check that all dependencies are installed
- Verify Google Cloud project configuration
- Review console output for error messages
- Ensure credentials and tokens are valid
