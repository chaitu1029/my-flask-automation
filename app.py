import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.remote_connection import RemoteConnection
from requests.exceptions import ReadTimeout

def run_selenium():
    logging.info("Selenium automation started")
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.binary_location = "/usr/bin/google-chrome"

        service = Service(executable_path="/usr/local/bin/chromedriver")

        # Increase HttpConnection timeout from default (60s) to 300s (5 mins)
        RemoteConnection._CONNECTION_TIMEOUT = 300

        driver = webdriver.Chrome(service=service, options=options)

        driver.get("https://example.com")
        logging.info(f"Page title: {driver.title}")

        # Add any additional automation steps here

        driver.quit()
        logging.info("Selenium automation finished successfully")

    except ReadTimeout as rt:
        logging.error(f"Selenium ReadTimeout error: {rt}", exc_info=True)
        # Optionally, you could restart the driver here or handle cleanup

    except Exception as e:
        logging.error(f"Selenium error: {e}", exc_info=True)
