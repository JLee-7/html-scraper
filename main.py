from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import os
import csv
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd



def auth():
    # Open login page
    driver.get('LOGIN URL')
    print("Opened login page")

    # Locate the username, password fields, and login button
    username = driver.find_element(By.ID, 'email')
    password = driver.find_element(By.ID, 'password')
    login_button = driver.find_element(By.ID, 'signin_btn')


    # Enter login credentials
    # Read credentials from environment variables to avoid hardcoding.
    # Set SCRAPER_USERNAME and SCRAPER_PASSWORD in your environment or .env file.
    user = os.environ.get("SCRAPER_USERNAME")
    pwd = os.environ.get("SCRAPER_PASSWORD")
    if not user or not pwd:
        raise RuntimeError("Please set SCRAPER_USERNAME and SCRAPER_PASSWORD environment variables")
    username.send_keys(user)
    password.send_keys(pwd)

    login_button.click()

    # Wait for page to load and check current URL to verify login
    WebDriverWait(driver, 10).until(EC.url_changes('LOGIN URL'))
    current_url = driver.current_url
    if 'password' in current_url:
        print("Login failed: still on login page")
    else:
        print("Login successful")

# URLs To be Scraped
def channel_thread_list():
    # Replace these placeholder URLs with real channel/thread URLs (commas required between entries).
    threads = [
        "URL_1",
        "URL_2",
        "URL_3",
    ]
    return threads

# Scrapes Given URLs for Names, Message Content, and Dates
def scrape(channels,names_list, text_list, dates_list):
    driver.get(channels)

    #Selects drop down for choosing Dates
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//button[contains(@class, "c-message_list__day_divider__label__pill")]'))).click()
    #Try to Select option for "Last Week"
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class = 'c-menu_item__label' and contains(.,'Last week')]"))).click()
    except:
        print("no messages this week")
    else:

        time.sleep(3)

        #Scrape Names
        names = driver.find_elements(by= "xpath", value='//span[contains(@class, "offscreen")]')
        for name in names:
            label = name.text
            if label:
                print(label)
                names_list.append(label)

        #Scrape Message Content
        texts = driver.find_elements(By.CLASS_NAME,"c-message__message_blocks--rich_text")
        for msg in texts:
            label = msg.text
            if label:
                print(label)
                text_list.append(label.strip().lower())

        #Scrape Dates
        dates = driver.find_elements(by="xpath", value= "//a[contains(@class, 'c-timestamp') and @data-ts]")
        for day in dates:
            label = day.get_attribute("aria-label")
            if label:  # Ensure the attribute exists
                print(label)
                dates_list.append(label)

        return names_list, text_list, dates_list

#Create CSV file containing the scraped data
def df_builder(names, text, dates):
    # Build a DataFrame from lists and save to CSV
    df = pd.DataFrame({"Names": names, "Text": text, "Dates": dates})
    df.to_csv("messages3.csv", index=False)
    print("Saved messages3.csv")


if __name__ == "__main__":
    # Initialize Chrome WebDriver using webdriver-manager to auto-download the correct driver.
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    dates_list = []
    names_list = []
    text_list = []
    auth()
    for url in channel_thread_list():
        scrape(url, names_list, text_list, dates_list)

    df_builder(names_list, text_list, dates_list)
    driver.quit()


