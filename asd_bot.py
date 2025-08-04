from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time
import requests
from bs4 import BeautifulSoup
import urllib.parse
import random
import undetected_chromedriver as uc
import os
import shutil
from urllib.parse import urlparse

from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService


def initial_proxy_driver():
    # Bright Data proxy details
    proxy_host = "brd.superproxy.io"
    proxy_port = 33335
    customer_id = "hl_d7e6dbf3"
    zone = "datacenter_proxy1"
    password = "imksvz685uzj"

    proxy_username = f"brd-customer-{customer_id}-zone-{zone}"
    proxy_password = password

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--ignore-ssl-errors")
    chrome_options.add_argument("--allow-insecure-localhost")
    chrome_options.add_argument("--disable-web-security")
    # chrome_options.add_argument("--headless")  # Optional
    chrome_options.add_argument("--disable-gpu")

    seleniumwire_options = {
        "proxy": {
            "http": f"http://{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}",
            "https": f"https://{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}",
        },
        "exclude_hosts": [
            "accounts.google.com",
            "www.googletagmanager.com",
            "www.google-analytics.com",
            "fonts.googleapis.com",
            "fonts.gstatic.com",
            "ssl.google-analytics.com",
            "asdinpreschool.eu",
            "region1.google-analytics.com",
            "update.googleapis.com",  # optionally exclude your main site if it's not loading properly
        ],
    }

    driver = webdriver.Chrome(
        options=chrome_options, seleniumwire_options=seleniumwire_options
    )

    return driver


def initial_download_driver(headless=True):
    options = Options()
    if headless:
        # Chrome 109+ new headless
        options.add_argument("--headless=new")

    download_dir = os.path.join(os.getcwd(), "asd_downloads")
    os.makedirs(download_dir, exist_ok=True)
    print("dir:", download_dir)

    options.add_argument("--start-maximized")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
    )
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option('prefs', {
        "download.default_directory": download_dir, 
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True
    })
    
     # Create the Selenium Service correctly (from selenium.webdriver, not seleniumwire)
    try:
        # Newer Selenium: supports log_output (file-like or path)
        service = ChromeService(log_output=open("selenium.log", "w"))
    except TypeError:
        # Older Selenium: fallback to log_path
        service = ChromeService(log_path="selenium.log")

    # Use Selenium Wire's Chrome but pass the Selenium Service + Options
    driver = webdriver.Chrome(service=service, options=options)

    # Hide webdriver flag (some sites detect automation)
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )

    # (Optional) For older Chrome headless, ensure downloads are allowed via CDP:
    try:
        driver.execute_cdp_cmd(
            "Page.setDownloadBehavior",
            {"behavior": "allow", "downloadPath": download_dir},
        )
    except Exception:
        pass

    return driver

def initial_general_driver():
    options = Options()
    options.add_argument("start-maximized")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
    )
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option(
        "prefs",
        {
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True,
        },
    )
    driver = webdriver.Chrome(options=options)
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )

    return driver

def clear_download_directory():
    download_dir = os.path.join(os.getcwd(), "asd_downloads")
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

def asd_unique_bot():
    driver = initial_proxy_driver()
    try:
        driver.get("https://api.ipify.org?format=text")
        time.sleep(2)
        proxy_ip = driver.find_element("tag name", "body").text
        print("Proxy IP:", proxy_ip)
        driver.get("https://asdinpreschool.eu")
        time.sleep(5)
    finally:
        driver.quit()

# asd_unique_bot()

def asd_visitor():
    driver = initial_general_driver()
    try:
        driver.get("https://asdinpreschool.eu")
        time.sleep(2)
        menu_items = driver.find_elements(By.CLASS_NAME, "uk-navbar-nav li a")
        for i, item in enumerate(menu_items):
            print(i, item.text)
            item.click()
            time.sleep(2)
            driver.back()
            time.sleep(2)

    except Exception as e:
        print(e)
    finally:
        driver.quit()
    
# asd_visitor()

def asd_download():
    driver = initial_download_driver()
    try:
        driver.get("https://asdinpreschool.eu/resources/")
        cookie_btn = driver.find_element(By.CSS_SELECTOR , '.js-accept')
        driver.execute_script("arguments[0].click();", cookie_btn)
        time.sleep(2)

        grid_items = driver.find_elements(By.CSS_SELECTOR, ".grid-res > div")
        for item in grid_items:
            print(item.text)
            # pending download action once we confirm the buttons

        driver.get("https://asdinpreschool.eu/category/news/")
        time.sleep(2)

        items = driver.find_elements(By.CSS_SELECTOR, '.news-grid .el-item a')
        for item in items:
            print(item.text)
            try:
                # Get the href attribute to see what URL we're clicking
                href = item.get_attribute('href')
                print(f"News item URL: {href}")
                
                driver.execute_script("arguments[0].click();", item)
                time.sleep(3)  # Increased wait time
                
                # Check if we're on the correct page
                current_url = driver.current_url
                print(f"Current URL: {current_url}")
                
                # Try to find the download button with multiple selectors
                download_btn = None
                selectors = [
                    '.inner-newslette-row .el-content.uk-button.uk-button-default',
                    '.uk-button.uk-button-default',
                    'a[href*=".pdf"]',
                ]
                
                for selector in selectors:
                    try:
                        download_btn = driver.find_element(By.CSS_SELECTOR, selector)
                        print(f"Found download button with selector: {selector}")
                        break
                    except:
                        continue
                
                if download_btn:
                    # Get the href or download attribute
                    download_url = download_btn.get_attribute('href')
                    print(f"Download URL: {download_url}")
                    
                    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", download_btn)
                    driver.save_screenshot("asd_news_before_click.png")
                    time.sleep(2)
                    
                    download_dir = os.path.join(os.getcwd(), "asd_downloads")
                    files_before = os.listdir(download_dir) if os.path.exists(download_dir) else []
                    print(f"Files before click: {files_before}")
                    
                    # Try direct download if browser download failed
                    if download_url and download_url.startswith('http'):
                        print("Attempting direct download...")
                        direct_result = download_pdf_direct(download_url)
                        if direct_result:
                            print(f"Direct download successful: {direct_result}")
                        else:
                            print("Direct download also failed")
                        
                        
                        
                else:
                    print("No download button found with any selector")
                    
            except Exception as e:
                print(e)

    except Exception as e:
        print(e)
    finally:
        # clear_download_directory()
        driver.quit()

def download_pdf_direct(url, filename=None):
    try:
        
        # Create download directory if it doesn't exist
        download_dir = os.path.join(os.getcwd(), "asd_downloads")
        os.makedirs(download_dir, exist_ok=True)
        
        # Get filename from URL if not provided
        if not filename:
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path)
            if not filename.endswith('.pdf'):
                filename += '.pdf'
        
        file_path = os.path.join(download_dir, filename)
        
        print(f"Downloading PDF from: {url}")
        print(f"Saving to: {file_path}")
        
        # Download the file
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"Successfully downloaded: {filename}")
        return file_path
        
    except Exception as e:
        print(f"Error downloading PDF directly: {e}")
        return None

asd_download()