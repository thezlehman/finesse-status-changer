Cisco Finesse Status Changer
This project provides a Python script to log into Cisco Finesse, change the agent status, and maintain the session using cookies. It includes a GUI for selecting the desired status and prompts for login credentials if they are not saved.

Features
Logs into Cisco Finesse and changes agent status.
Saves and loads cookies to maintain session.
Encrypts and stores login credentials in a .env file.
Provides a GUI for selecting the agent status.
Prompts for login credentials if not saved.
Dynamically updates the GUI with the current status and available status options.
Generates a random encryption key on the first start and saves it to the .env file.
Allows toggling headless mode in real-time from the GUI.
Supports changing status using command-line arguments after starting the script.
Requirements
Python 3.x
selenium
webdriver-manager
python-dotenv
cryptography
pickle-mixin
Installation
Clone the repository:
git clone https://github.com/thezlehman/cisco-finesse-status-changer.git
cd cisco-finesse-status-changer

Install the required packages:
pip install -r requirements.txt

Create a .env file with the following content:
FINESSE_URL=
FINESSE_USERNAME=
FINESSE_PASSWORD=
FINESSE_EXTENSION=
ENCRYPTION_KEY=

The script will generate a random encryption key on the first start and save it to the .env file.
Usage
Run the script:
python statuschange.py

If the credentials are not saved in the .env file, a GUI will prompt you to enter and save them.
After logging in, a GUI will allow you to select the desired agent status and update the current status.
Toggle Headless Mode: Use the checkbox in the GUI to switch between headless and non-headless modes in real-time.
Change Status Using Arguments: You can change the agent status by running the script with a status argument. For example:
python statuschange.py -lunch

This will change the agent status to “Lunch”. 



Notes
Ensure that the WebDriver (e.g., ChromeDriver) is compatible with your browser version.
The script runs in non-headless mode by default. Use the checkbox in the GUI to toggle headless mode.


License
This project is licensed under the MIT License.