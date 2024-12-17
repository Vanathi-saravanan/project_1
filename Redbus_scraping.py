from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import sqlite3

from datetime import datetime

# Function to scrape data from Redbus
def collect_data():

    buses = redbus_data_scraping()
    return pd.DataFrame(buses, columns=['route_name', 'busname', 'bustype', 'departing_time','departing_loc', 'duration', 'reaching_time', 'reaching_loc','star_rating', 'price', 'seats_available','route_link',])

# Data scraping using selenium with firefox driver
def redbus_data_scraping():
    driver = webdriver.Firefox()
    driver.maximize_window()

    driver.get('https://www.redbus.in/')
    print('Start processing data scraping from redbus')
    cityA = 'chennai'
    cityB = 'bangalore'
    dateGiven = '22/07/2024'

    # Example: Search for buses between two cities
    WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//label[contains(text(),'From')]//preceding-sibling::input"))
    )
    driver.find_element(By.XPATH, "//label[contains(text(),'From')]//preceding-sibling::input").clear
    driver.find_element(By.XPATH, "//label[contains(text(),'From')]//preceding-sibling::input").send_keys(cityA)

    WebDriverWait(driver, 90).until(
        EC.element_to_be_clickable((By.XPATH, "//li[contains(@class,'cursorPointing')]/div/text"))
    )

    driver.find_element(By.XPATH,"//li[contains(@class,'cursorPointing')]/div/text").click()
    
    # Example: Search for buses between two cities
    WebDriverWait(driver, 90).until(
        EC.visibility_of_element_located((By.XPATH, "//label[contains(text(),'To')]//preceding-sibling::input"))
    )
    driver.find_element(By.XPATH, "//label[contains(text(),'To')]//preceding-sibling::input").clear
    driver.find_element(By.XPATH, "//label[contains(text(),'To')]//preceding-sibling::input").send_keys(cityB)
    driver.find_elements(By.XPATH,"//text[contains(text(),'"+cityB+"')]")

    WebDriverWait(driver, 90).until(
        EC.element_to_be_clickable((By.XPATH, "//li[contains(@class,'cursorPointing')]/div/text"))
    )

    driver.find_element(By.XPATH,"//li[contains(@class,'cursorPointing')]/div/text").click()
   
    # Convert dateGiven string to datetime.date object
    date1 = datetime.strptime(dateGiven, "%d/%m/%Y").date()

    # Get current date as datetime.date object
    date2 = datetime.now().date()

    delta = date1 - date2
    # Calculate the difference in days
    differenceDate = delta.days

    if(differenceDate>60 or differenceDate<0):
        print("Invalid date. It should be from today to 60 days")
    else:
        monthNameGiven = date1.strftime('%b')
        monthNameFrmCal = driver.find_element(By.XPATH,"//div[contains(@class,'DayNavigator') and contains(@style,'font')]").text

    dateGivenArr = dateGiven.split(",")
    if(monthNameGiven in monthNameFrmCal) :
        driver.find_element(By.XPATH,"//span[contains(@class,'DayTiles__CalendarDaysSpan') and text()='" + dateGiven.split("/")[0] + "']").click()

    driver.find_element(By.XPATH,"//button[text()='SEARCH BUSES']").click();
    
    # Extract bus details
    buses = []

    WebDriverWait(driver, 90).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(@class,'busFound')]"))
    )

    busCount = int(driver.find_element(By.XPATH, "//span[contains(@class,'busFound')]").text.split(" ")[0])

    for x in range(1, busCount):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    WebDriverWait(driver, 90).until(
        EC.visibility_of_element_located((By.XPATH, "//ul[contains(@class,'bus-items')]/div["+str(busCount-1)+"]"))
    )
    bus_elements = driver.find_elements(By.XPATH, "//ul[contains(@class,'bus-items')]/div")
    print('Total number of bus:',busCount)
    for i in range(1, int(busCount)):
        route_name = cityA +' to '+cityB
        busname = driver.find_element(By.XPATH, "(//div[contains(@class,'travels')])["+str(i)+"]").text
        bustype = driver.find_element(By.XPATH, "(//div[contains(@class,'bus-type')])["+str(i)+"]").text
        departing_time = driver.find_element(By.XPATH, "(//div[contains(@class,'dp-time')])["+str(i)+"]").text
        departing_loc = driver.find_element(By.XPATH, "(//div[contains(@class,'dp-loc')])["+str(i)+"]").text
        duration = driver.find_element(By.XPATH, "(//div[contains(@class,'dur')])["+str(i)+"]").text
        reaching_time = driver.find_element(By.XPATH, "(//div[contains(@class,'bp-time')])["+str(i)+"]").text
        reaching_loc = driver.find_element(By.XPATH, "(//div[contains(@class,'bp-loc')])["+str(i)+"]").text
        star_rating = driver.find_element(By.XPATH, "(//div[contains(@class,'rating-sec')]//span)["+str(i)+"]").text
        try:
            star_rating = driver.find_element(By.XPATH, "(//div[contains(@class,'rating-sec')]//span)[" + str(i) + "]").text
        except NoSuchElementException:
            star_rating = "No rating"
        price =  driver.find_element(By.XPATH, "(//div[contains(@class,'fare')]//span)["+str(i)+"]").text
        seats_available = driver.find_element(By.XPATH, "(//div[contains(@class,'seat-left')])["+str(i)+"]").text
        route_link = driver.current_url
        buses.append([route_name,  busname, bustype, departing_time, departing_loc, duration, reaching_time, reaching_loc, star_rating, price, seats_available,route_link,])
        print("Number of bus data collected: ",i)
    driver.quit()
    print("Data scraping process completed")
    return buses

# Function to save data to SQLite database
def save_to_db(data):
    conn = sqlite3.connect('Redbus.db')
    data.to_sql('bus_routes', conn, if_exists='replace', index=False)
    conn.commit()
    print('Data saved in sqlite database')
    conn.close()

if __name__ == "__main__":
    redbus_data = collect_data()
    save_to_db(redbus_data)
    print("Data scraped and saved to database successfully.")


