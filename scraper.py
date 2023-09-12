from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import time
import sqlite3
import pandas as pd


def highlight(element, color, border):
    driver = element._parent

    def apply_style(s):
        driver.execute_script(
            "arguments[0].setAttribute('style', arguments[1]);", element, s
        )

    original_style = element.get_attribute("style")
    apply_style("border: {0}px solid {1};".format(border, color))
    time.sleep(0.01)
    apply_style(original_style)


chrome_options = Options()
chrome_options.add_argument("--headless=new")
PATH = ".\chromedriver_win64\chromedriver.exe"  # C:\Users\harik\OneDrive\Desktop\dsclubb\openai\chromedriver_win64
service = Service(PATH)
driver = webdriver.Chrome(
    service=service, options=chrome_options
)  # options=chrome_options
driver.get("https://uconntact.uconn.edu/organizations")
time.sleep(3)

while True:
    try:
        load = driver.find_element(By.CSS_SELECTOR, ".outlinedButton")
        load.click()
        time.sleep(0.5)
    except:
        break
