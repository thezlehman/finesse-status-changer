import tkinter as tk
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pickle
import os
import time
from dotenv import load_dotenv, set_key
import base64
from cryptography.fernet import Fernet
import getpass

# Load environment variables
load_dotenv()

# Generate a random encryption key if not present
if not os.getenv('ENCRYPTION_KEY'):
    key = Fernet.generate_key()
    set_key('.env', 'ENCRYPTION_KEY', key.decode())
else:
    key = os.getenv('ENCRYPTION_KEY').encode()

cipher_suite = Fernet(base64.urlsafe_b64encode(key))

# Replace these variables with your actual Finesse details
finesse_url = os.getenv('FINESSE_URL')
username = os.getenv('FINESSE_USERNAME')
encrypted_password = os.getenv('FINESSE_PASSWORD')
extension = os.getenv('FINESSE_EXTENSION')
cookie_file = 'cookies.pkl'

def save_cookies(driver, path):
    with open(path, 'wb') as filehandler:
        pickle.dump(driver.get_cookies(), filehandler)

def load_cookies(driver, path):
    with open(path, 'rb') as cookiesfile:
        cookies = pickle.load(cookiesfile)
        for cookie in cookies:
            driver.add_cookie(cookie)

def change_status(driver, status):
    try:
        # Click on the status dropdown
        driver.find_element(By.ID, 'voice-state-select-headerOptionText').click()
        # Select the desired status option
        driver.find_element(By.XPATH, f"//div[contains(text(), '{status}')]").click()
        print(f"Status changed to {status} successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

def login_and_setup_driver():
    # Set up Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Initialize the WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        # Navigate to the Finesse login page
        driver.get(finesse_url)
        
        # Load cookies if they exist
        if os.path.exists(cookie_file):
            load_cookies(driver, cookie_file)
            driver.refresh()
        else:
            # Decrypt the password
            password = cipher_suite.decrypt(encrypted_password.encode()).decode()

            # Log in to Finesse
            driver.find_element(By.ID, 'username').send_keys(username)
            driver.find_element(By.ID, 'extension').send_keys(extension)
            driver.find_element(By.ID, 'password').send_keys(password)
            driver.find_element(By.ID, 'signin-button').click()
            
            # Wait for the page to load
            time.sleep(5)
            
            # Save cookies
            save_cookies(driver, cookie_file)
        
        return driver
        
    except Exception as e:
        print(f"An error occurred during login: {e}")
        driver.quit()
        return None

def create_gui(driver):
    def on_status_change(event):
        selected_status = status_combobox.get()
        change_status(driver, selected_status)

    def update_status():
        try:
            current_status = driver.find_element(By.ID, 'voice-state-select-headerOptionText').text
            status_label.config(text=f"Current Status: {current_status}")
        except Exception as e:
            status_label.config(text="Error fetching status")

    def populate_status_options():
        try:
            # Click on the status dropdown to reveal options
            driver.find_element(By.ID, 'voice-state-select-headerOptionText').click()
            time.sleep(1)  # Wait for the dropdown to populate

            # Find all status options
            status_elements = driver.find_elements(By.XPATH, "//div[@role='option']")
            statuses = [element.text for element in status_elements]

            # Populate the combobox with the statuses
            status_combobox['values'] = statuses
        except Exception as e:
            print(f"An error occurred while populating status options: {e}")

    root = tk.Tk()
    root.title("Cisco Finesse Status Changer")

    ttk.Label(root, text="Select Status:").grid(column=0, row=0, padx=10, pady=10)

    status_combobox = ttk.Combobox(root)
    status_combobox.grid(column=1, row=0, padx=10, pady=10)
    status_combobox.bind("<<ComboboxSelected>>", on_status_change)

    status_label = ttk.Label(root, text="Current Status: ")
    status_label.grid(column=0, row=1, columnspan=2, padx=10, pady=10)

    update_button = ttk.Button(root, text="Update Status", command=update_status)
    update_button.grid(column=0, row=2, columnspan=2, padx=10, pady=10)

    populate_button = ttk.Button(root, text="Populate Status Options", command=populate_status_options)
    populate_button.grid(column=0, row=3, columnspan=2, padx=10, pady=10)

    root.mainloop()

def prompt_for_credentials():
    def save_credentials():
        global username, extension, encrypted_password
        username = username_entry.get()
        extension = extension_entry.get()
        password = password_entry.get()
        encrypted_password = cipher_suite.encrypt(password.encode()).decode()

        with open('.env', 'a') as f:
            f.write(f'FINESSE_USERNAME={username}\n')
            f.write(f'FINESSE_PASSWORD={encrypted_password}\n')
            f.write(f'FINESSE_EXTENSION={extension}\n')

        credentials_window.destroy()

    credentials_window = tk.Tk()
    credentials_window.title("Enter Cisco Finesse Credentials")

    ttk.Label(credentials_window, text="Username:").grid(column=0, row=0, padx=10, pady=10)
    username_entry = ttk.Entry(credentials_window)
    username_entry.grid(column=1, row=0, padx=10, pady=10)

    ttk.Label(credentials_window, text="Extension:").grid(column=0, row=1, padx=10, pady=10)
    extension_entry = ttk.Entry(credentials_window)
    extension_entry.grid(column=1, row=1, padx=10, pady=10)

    ttk.Label(credentials_window, text="Password:").grid(column=0, row=2, padx=10, pady=10)
    password_entry = ttk.Entry(credentials_window, show="*")
    password_entry.grid(column=1, row=2, padx=10, pady=10)

    save_button = ttk.Button(credentials_window, text="Save", command=save_credentials)
    save_button.grid(column=0, row=3, columnspan=2, padx=10, pady=10)

    credentials_window.mainloop()

if __name__ == "__main__":
    if not username or not encrypted_password or not extension:
        prompt_for_credentials()
    driver = login_and_setup_driver()
    if driver:
        create_gui(driver)
