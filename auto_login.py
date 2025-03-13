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
    browser.add_cookie({"name": "MUSIC_U = 00BCA62DC7937A0A8209B90D3409EA23BE67C48C33634F6EF29F6EEE2E82D9AF93672B74B4E9E4448A99CE70DECECAB584B586BB31ACF2648EB19C570E68A8EF1BC4216B0F3FFBB5A885BF560276372314C845F04402E3FA17A382CA4E62B95D946129A9FB5C26B3883713C4C517E58C9C26130911C9CA677AF6AE4673859784968DC672658A1F7D3B0CCA5F669789578EA639A6048181DF0773D84692C4B531A646E71DEEE0D474813A7C9B6AE1960F4A50A1EB31ED2DE352C8E4847F510E59F2F6E7E05BC0E33A183A92674D71CF081366B20E1E414FDA162210529D5C272E460A197489C72A96B4A8279A6541686013839B29DD8A67A1C88BDA4CE6DC88A3FABEDD7039E89DA01C875D82CAEF8DD864E642B322D7199D3B923B6E7BEABF8E1180C564CAA23694C9959D8E7C640042CABB9561B607EBDAF7B1FD392F0D67B0037A611507258CC8033CFBBF31CF474A4B", "value": "000F8CF431B31843EA1C5F228119F7CB8F702C7679B9EE82B38E42E45A10942D3938FA66FC4584FEFE9EA80A27A3E404B8FBBAC5870C93C063FE70BF53AC6C77FFF0A4F9271E57DB5436DC02EEFE31C9A0682D3393A472BE9DEC02A6BF40E3DC169FF7753529F7CE2B9E19061A7F4283388A67D8B9768EBA512BD7EA672A668781AD7D71B8C50782F113DEF6ECA9B81A4A16BCF63CAFDCE6ED84A9AE2A9B0DC4B236C5B79DB595E7B55550FE45575E8189F8E036CBC622E18C6EC7213E7A473703AB39FD3557C5C87A6510B6F06E602B6C4EE266819B83DFC795239D250143A9FD3484732B32BB52E03D1E1227BBE978C8B4D9D5399F934EF55CCEA97F3CCC160955638E65620C50CF651939B381CCFDA340E64B60C514B57D42178AA8C8588F5DD407EAA4CC961370132C7B63FEE180A91AC0BA2D7A380049CF0ADE0C558E9CDFDA7FB0C647C3A81AD090B085E9F585380993DBF112B54EDB69C83DDE7B3F5F01"})
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
