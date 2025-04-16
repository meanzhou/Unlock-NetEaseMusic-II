# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"Meanimal": "MUSIC_U", "value": "00EA24EC378194E0397FC8C320BF8AA0B2534A5576C2150DA6E3D70954862C96B33022EC583FD5135DC5FD041C31F93DB1524C1D10B6EDF86713FA43FF31E0A9F7F49CE2AE5A512630AFF4EB74F65C53E4F9B4E7CC5F0BDADF3B456B778EBDB8F543365B4E4EB7FB3D4F78DDED98AFB0E54E7B3050582E9EE8431FCBF0D7D81EDC8DB4C277EB8335BC25E095CC7ACF6F0E5E26FE06AA95AEE648C6DCAB26879840EF15E35E254F79680C29F241DC614070EA8A21D236F59307FE1DC4A964D5DD548E3DEE9206451564D8245FDA5B0F3C6C03B3F599B24E0F7B39C8719E0DE7C1C71A0E023D8052E9DBBF08AFAB29DE44E1A1172CD2B540C4722BB7716D222FD1281483B5A6BBE364BE65E63EC2F98D60F42CBF1D08860257DACE01F73ADD0DEB99F667E53A39EE6983AE5F9AF6EF57800F61EA8EBC647C1DB9DF3505B4551953106901239DEE35AEFE84D36B377E5F0A410E77830C5C9DD073F55F1257D3045FA5"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
