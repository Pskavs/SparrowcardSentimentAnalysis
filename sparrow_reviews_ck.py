#Importing packages and setting up selenium.
import os
from time import sleep
import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from dotenv import load_dotenv

# Sets email and password
load_dotenv()
EMAIL = os.environ.get("EMAIL")
PASS = os.environ.get("PASS")

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
chrome_options.add_argument("--incognito")

driver = webdriver.Chrome(options = chrome_options)
driver.get("https://www.creditkarma.com/reviews/credit-card/single/id/ccsparrowcard01")

def login():
    """"
    This function will login to Sparrow Reviews on Credit Karma.
    """
    sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight - 1500);")
    sleep(1)
    driver.find_element(By.XPATH, '//*[@id="main"]/div[6]/div/p/a').click()

    # When the all member reviews link is clicked, a new tab is opened so we have to switch to that tab.
    current_window = driver.current_window_handle
    all_windows = driver.window_handles
    for window in all_windows:
        if window != current_window:
            driver.switch_to.window(window)
    sleep(1)
    # Enters the email and password and then logs in.
    sleep(2)
    driver.find_element(By.XPATH, '//*[@id="username"]').send_keys(EMAIL)
    sleep(2)
    driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(PASS)
    sleep(2)
    driver.find_element(By.XPATH, '//*[@id="Logon"]').click()
    sleep(4)
    driver.find_element(By.XPATH, '// *[ @ id = "two-factor-auth"] / div / div[1] / button').click()
    sleep(8)


def save_html():
    """
    Saves the html pages to a file which will later be scraped. After each file is saved, it will go to the next page.
    """
    count = 1
    #There are 22 pages of reviews on CK.
    while count < 22:
        inner_html = driver.page_source
        with open(f"ck_scrapes/html{count}.txt", "w", encoding="utf-8") as file:
            file.write(inner_html)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight - 1500);")
        sleep(3)
        driver.find_element(By.CSS_SELECTOR, '#__render-farm > div > div > div > main > div.jsx-1897936934.center.w-100.mw8.flex.overflow-hidden.justify-between > div.jsx-1897936934.w-100.reviews-column.flex.flex-column > div.mw8.center.bg-white.flex.flex-row.items-center.justify-center.mt0.mb3 > div:nth-child(3) > svg').click()
        sleep(2)
        count += 1

login()
save_html()