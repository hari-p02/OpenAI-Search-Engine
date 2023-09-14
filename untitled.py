from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import time
import sqlite3
import pandas as pd

chrome_options = Options()
chrome_options.add_argument("--headless=new")
PATH = ".\chromedriver_win64\chromedriver.exe"  # C:\Users\harik\OneDrive\Desktop\dsclubb\openai\chromedriver_win64
service = Service(PATH)
driver = webdriver.Chrome(
    service=service, options=chrome_options
)  # options=chrome_options
driver.get("https://uconntact.uconn.edu/organization/co4hvernon")
time.sleep(3)


load = driver.find_element(By.CSS_SELECTOR, "img")


