from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
from bs4 import BeautifulSoup
import urllib.parse
import random
import undetected_chromedriver as uc
import os
import shutil

def init_download_driver(headless=True):
    options = Options()
    if headless:
        options.add_argument("--headless=new")

    download_dir = os.path.join(os.getcwd(), "shore_downloads")
    # Create download directory if it doesn't exist
    os.makedirs(download_dir, exist_ok=True)
    print("dir: " + download_dir)
    # download_dir = "D:\Desktop\Bokis\ForMe\Python\Projects\qa_crew\shore_downloads"
    
    options.add_argument("start-maximized")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option('prefs', {
        "download.default_directory": download_dir, 
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True
    })
    # service = webdriver.ChromeService(log_output='selenium.log')
    driver = webdriver.Chrome(options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    return driver

def clear_download_directory():
    download_dir = os.path.join(os.getcwd(), "shore_downloads")
    if os.path.exists(download_dir):
        for filename in os.listdir(download_dir):
            file_path = os.path.join(download_dir, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Error deleting {file_path}: {e}')
    print('Download directory cleared')

def download_file():
    driver = init_download_driver()

    urls = [
        "https://shorewinner.eu/reports-and-publications/",
        "https://shorewinner.eu/dgfdg/"
    ]
    try:
        for i,url in enumerate(urls):
            driver.get(url)
            time.sleep(1)
            # driver.save_screenshot("shore_before.png")
            if i == 0:
                cookie_btn = driver.find_element(By.CSS_SELECTOR , '.js-accept')
                driver.execute_script("arguments[0].click();", cookie_btn)
                time.sleep(2)
                # driver.save_screenshot("shore_after_cookie.png")
            # WebDriverWait(driver, 10).until(
            #     EC.presence_of_element_located((By.CSS_SELECTOR, 'a.uk-button-primary'))
            # )
            footer = driver.find_element(By.ID , 'builderwidget-3')
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", footer)
            time.sleep(2)
            # driver.save_screenshot("shore_footer.png")
            if url == "https://shorewinner.eu/reports-and-publications/":
                btns = driver.find_elements(By.LINK_TEXT, 'View as PDF')
                print('found: ' + str(len(btns)))
            else:
                btns = driver.find_elements(By.LINK_TEXT, 'Download as PDF')
                print('found: ' + str(len(btns)))

            try:
                for i,btn in enumerate(btns):
                    print('starts with btn:' + str(i))
                    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", btn)
                    time.sleep(2)
                    driver.execute_script("arguments[0].click();", btn)
                    time.sleep(1)
                    
                    # driver.switch_to.window(driver.window_handles[1])
                    # time.sleep(15)
                    # driver.save_screenshot("shore_switch_window-"+str(i)+".png")
                    # download_btn = driver.find_element(By.ID, 'download')
                    # driver.execute_script("arguments[0].click();", download_btn)
                    # time.sleep(1)
                    # driver.save_screenshot("shore_sleep_after_click-"+str(i)+".png")
                    print('clicked')


            except Exception as e:  
                print(f"Error during clicking: {str(e)}")
            
        # driver.save_screenshot("shore_after_click.png")
    except Exception as e:
        print(f"Error during loading page: {str(e)}")
    finally:
        time.sleep(2)  
        clear_download_directory()
        driver.quit()


download_file()