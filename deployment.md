# Streamlit Cloud Deployment Guide

This guide details how to deploy your **Job Vacancy Search System** to Streamlit Cloud.

## Prerequisites
1. **GitHub Repository**: Your code must be pushed to GitHub (which we have done).
2. **Streamlit Account**: Sign up at [share.streamlit.io](https://share.streamlit.io/).

## Configuration Files
The following files are Critical for the deployment to work:
- **`requirements.txt`**: Lists Python libraries (`selenium`, `streamlit`, etc.).
- **`packages.txt`**: Lists system dependencies (`chromium`, `chromium-driver`). **Crucial for Selenium**.
- **`app.py`**: The main entry point. We have configured it to run in `headless=True` mode by default.

## Deployment Steps

1. **Login to Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io/) and login with your GitHub account.

2. **New App**
   - Click **"New app"**.
   - Select your valid repository: `AnkushGitRepo/Internship_Task`.
   - Branch: `main`.
   - Main file path: `app.py`.

3. **Deploy!**
   - Click **"Deploy"**.
   - Streamlit will install the dependencies from `requirements.txt` and `packages.txt`.
   - This process may take 2-3 minutes.

## Troubleshooting

### "WebDriverException: Message: Service /usr/bin/chromedriver unexpectedly exited"
- This rarely happens with the current setup, but if it does, it means `chromium-driver` isn't found. Ensure `packages.txt` exists in the root.

### "DevToolsActivePort file doesn't exist" / Crash
- This implies the browser tried to open a GUI.
- **Fix**: Ensure `NCSScraper(headless=True)` is set in `app.py`.

### "No jobs found" (NCS)
- Expected behavior on cloud IPs due to strict geo-blocking or bot detection.
- The `app.py` has a fallback: `st.warning("...Using mock data")` so the app won't crash, it will just show demo data.
