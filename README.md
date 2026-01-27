# Mail Automation Bot

Automates Gmail monitoring and Google Calendar alerts for reward registration and slot booking emails.

## What it does
- Authenticates with Gmail/Calendar via OAuth; stores tokens in `token.json` after first run.
- Watches unread messages every 30s.
- When an unread mail matches certain phrases:
  - "assessment registration" or "reward points" → creates two calendar reminders (now+4 minutes, and fixed 8:00 PM) and records completion in `reward_last_run.txt`.
  - "assessment booking" or "portal" → creates a reminder (now+4 minutes) and records completion in `slot_last_run.txt`.
- Marks processed messages as read to avoid reprocessing.

## File map
- [gmail_test.py](gmail_test.py): handles OAuth flow and token refresh.
- [reward_bot.py](reward_bot.py): main loop for Gmail polling and Calendar event creation.
- `credentials.json`: Google Cloud OAuth client secrets (user-provided).
- `token.json`: generated OAuth token cache after first auth.
- `*_last_run.txt`: date stamps to prevent duplicate alerts per day.

## Prerequisites
- Python 3.10+ recommended.
- Google Cloud project with Gmail API and Calendar API enabled.
- OAuth 2.0 Client ID (Desktop) JSON saved as `credentials.json` in repo root.

## Setup
1) Create and activate a virtual environment (Windows example):
```powershell
python -m venv mailenv
mailenv\Scripts\Activate.ps1
```

2) Install dependencies:
```powershell
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

3) Place your `credentials.json` in the project root. First run will open a browser to grant Gmail+Calendar scopes; `token.json` will be written afterward.

## Running
```powershell
python reward_bot.py
```
- Keep the terminal open; the bot polls Gmail every 30 seconds.
- Press Ctrl+C to stop cleanly.

## Customizing
- Update search phrases or reminder text in [reward_bot.py](reward_bot.py).
- Change the fixed 8 PM alert time via the `specific_hour` parameter in `create_alarm`.
- Adjust polling cadence by editing the `time.sleep(30)` interval.

## Notes & privacy
- Tokens are user-bound; rotate/delete `token.json` if access is revoked or scopes change.
- Ensure `credentials.json` and `token.json` are kept private (git-ignore them if committing code).
