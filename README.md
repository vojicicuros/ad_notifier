# KupujemProdajem Ad Notifier

## Overview

This Python script monitors new ads on kupujemprodajem.rs for specific search criteria and sends email notifications when new ads appear. It fetches ads based on a filtered URL, so all filters like keywords, price range, and categories are handled directly via the URL (KP_URL). The script keeps track of ads it has already seen in a seen_ads.txt file to avoid duplicate notifications.

---

## Features

- Periodically checks the specified Kupujemprodajem search page for new ads  
- Sends email notifications with details of new ads found  
- Persists seen ads in a local file to avoid repeated alerts  
- Fully configurable via environment variables  
- Runs silently in the background  

---

## Setup

1. Clone this repository

2. Install required libraries

pip install -r requirements.txt

Required libraries:  
- requests  
- beautifulsoup4  
- python-dotenv

3. Configure environment variables

- Copy .env_example to .env:

cp .env_example .env

- Edit .env and set your email credentials and SMTP server info.

4. Configure the URL

- **Change the KP_URL in the script to your desired filtered search URL from kupujemprodajem.rs**.  
- The website handles all filters via the URL, so you only need to update KP_URL to change what ads are monitored.

5. Seen Ads File

- The script saves IDs of seen ads in seen_ads.txt to avoid notifying about the same ads repeatedly.

---

## Running the Script

python your_script.py

---

## Running Automatically on Startup

### On Linux

1. Make the script executable (if needed):

chmod +x your_script.py

2. Add a cron job to run on reboot:

crontab -e

Add the following line:

@reboot /usr/bin/python3 /full/path/to/your_script.py &

Replace /usr/bin/python3 with your Python executable path if different.

---

### On Windows

Option 1: Add shortcut to Startup folder

- Create a shortcut that runs:

pythonw.exe "C:\full\path\to\your_script.py"

- Open Run dialog (Win + R), type:

shell:startup

- Paste the shortcut inside the opened Startup folder.

Option 2: Use Task Scheduler

- Open Task Scheduler and create a new task to run pythonw.exe with your script path at user logon.

  
