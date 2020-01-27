import sys
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import requests
import scipy
import stats
from PyAstronomy import pyasl
import datetime
from datetime import date, timedelta, datetime
import time
from time import sleep
import schedule
import os
import pickle


'''
Please ensure that within the command line, path your way to the folder contain the .py file.

This file can be run in command line with the following:

Argument 1 = cheapFlight_alerter.py Argument 2 = departure_destination (format = '') Argument 3 = arrival_destination (format = '') Argument 4 = start_date (format = 'YYYY-MM-DD') Argument 5 = end_date (format = 'YYYY-MM-DD') Argument 6 = city_key (format = ''), this is to check specific city with a continent.

For example ->

python cheapFlight_alerter.py 'Sydney' 'Europe' '2020-03-01' '2020-03-15' 'Edinburgh'
'''


def check_flights():
    # Step 1 - Initialise the Chromedriver:
    chromeDriver_file = 'chromedriver'
    chromeDriver_path = os.path.abspath(chromeDriver_file)
    browser = webdriver.Chrome(chromeDriver_path)

    # Step 2 - Scraping the Web Data:
    week_period = 26
    start_date = sys.argv[4]
    end_date = sys.argv[5]

    Adjust_delay = 50  # Adjust for internet connection. Default = 50
    check_time = 7  # 7 days is the default.\

    departure_destination = sys.argv[2]
    arrival_destination = sys.argv[3]

    # Format the flight dates: with the python datetime standard.
    startFlight_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    endFlight_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')

    # Dictionary for Fares:
    flightFare_dict = {}

    for idx in range(week_period):
        sat_start = str(startFlight_date).split()[0]
        sat_end = str(endFlight_date).split()[0]
        flightFare_dict.update({sat_start: {}})

        # Load webpage:
        sats = "https://www.google.com/flights?hl=en#flt=.." + sat_start + "*.." + sat_end + ";c:AUD;e:1;sd:1;t:h"
        sleep(np.random.randint(3, 7))
        browser.get(sats)
        print('Index: ' + str(
            idx) + ' Starting Browser and searching link: Google ' + browser.title + '. Dates are: ' + sat_start + ' and ' + sat_end + '.')

        # Input information to search for flights:
        wait_10sec = WebDriverWait(browser, 10)  # Seconds of Waiting.

        print('Link Loaded, Entering Travel Details now.')

        # Departure Search: input of departure location.
        departureDestination_link = wait_10sec.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="flt-app"]/div[2]/main[1]/div[4]/div/div[3]/div/div[2]/div[1]')))
        departureDestination_link.click()
        departureDestination_link = wait_10sec.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="sb_ifc50"]/input')))
        sleep(1)
        departureDestination_link.send_keys(departure_destination)
        sleep(2)
        departureDestination_link.send_keys(Keys.ENTER)

        # Arrival Search: input of arrival location.
        arrivalDestination = wait_10sec.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="flt-app"]/div[2]/main[1]/div[4]/div/div[3]/div/div[2]/div[2]')))
        arrivalDestination.click()
        arrivalDestination = wait_10sec.until(EC.presence_of_element_located((By.XPATH, '//*[@id="sb_ifc50"]/input')))
        sleep(1)
        arrivalDestination.send_keys(arrival_destination)
        sleep(2)
        arrivalDestination.send_keys(Keys.ENTER)

        # Get new URL:
        sleep(1)
        new_browser_url = browser.current_url
        print('After inputting the destinations and searching, the new URL is: \n' + new_browser_url)

        # Finally, click on the 'Search' button:
        floatingActionButton_click = browser.find_elements_by_xpath(
            '//*[@id="flt-app"]/div[2]/main[1]/div[4]/div/div[3]/div/div[4]/floating-action-button')[0]
        sleep(2)
        floatingActionButton_click.click()
        print('Search done. Next is to get a list of the travel information.')

        # Step 3 - Extract the relevant Data from the webpage:
        print('Collecting data. \n')
        sleep(Adjust_delay)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        flight_cards = soup.select('div[class*=MebuN]')

        for card in flight_cards:
            print('Extracting...')
            city = card.select('h3')[0].text
            fare = card.select('div[class*=MJg7fb]')[0].text.replace('Great value', "")
            flightFare_dict[sat_start] = {**flightFare_dict[sat_start], **{city: fare}}

        # Update the date: Add 7 days.
        startFlight_date = startFlight_date + timedelta(days=check_time)
        endFlight_date = endFlight_date + timedelta(days=check_time)

    browser.quit()
    print('Quiting Broswer, Data Collection Complete.')

    # Step 4 - Update the Dictionary:
    city_key = sys.argv[6]

    # Checks for City flights that may not be on certain dates and updates only with the existing values.
    count = 0
    for k, v in flightFare_dict.items():
        if (city_key) in v:
            count += 1

    city_dict = {}
    second_count = 0
    for k, v in flightFare_dict.items():
        second_count += 1
        if second_count == count:
            break
        city_dict.update({k: int(v[city_key].replace(',', '').split('$')[1])})

    # Plot the data:
    # Convert prices to integers:
    prices = [int(x) for x in city_dict.values()]

    # Extract the Date data from the dictionary:
    dates = city_dict.keys()

    # Step 5 - Outlier Detection:
    fare_prices = prices
    max_outliers = 3
    significance_lvl = 0.025

    r = pyasl.generalizedESD(fare_prices, max_outliers, significance_lvl, fullOutput=True)
    print('City -> ' + city_key)
    print('Total Outliers: ', r[0])

    # Print out data in regards to 'R' and Lambda: used to determine if data point is an outlier.
    out_dates = {}
    for i in sorted(r[1]):
        out_dates.update({list(dates)[i]: list(prices)[i]})

    # Check for lower prices:
    city_price_mean = np.mean(list(city_dict.values()))
    print('The mean price is: $%.2f' % city_price_mean + ' AUD')

    # Load in the API KEY
    IFTTT_key_folderName = 'IFTTT API key'
    IFTTT_path = os.path.abspath(IFTTT_key_folderName) + '/'

    IFTTT_API_KEY = open(IFTTT_path + "IFTTT API KEY.txt", 'r')
    api_key_string = []
    for i in IFTTT_API_KEY:
        api_key_string.append(str(i))

    for k, v in out_dates.items():
        if v < city_price_mean:
            requests.post('https://maker.ifttt.com/trigger/cheap_fares/with/key/' + api_key_string[0],
                          data={"value1": str(city_key), "value2": str(v), "value3": ""})
            print('Alert for', city_key + '!')
            print('Fare: $' + str(v), 'on', k)
            print('\n')
        else:
            print(str(v) + ' is greater than ' + str(city_mean))

# Step 6 - Scheduler to run code every 60mins:
schedule.every(60).minutes.do(check_flights)
while 1:
    schedule.run_pending()
    time.sleep(1)