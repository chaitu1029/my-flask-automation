import threading
from flask import Flask, render_template, redirect, url_for

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/')
def home():
    return render_template('index.html')

def run_selenium_script():
    logging.info("Selenium script started")
    options = Options()
    options.add_argument("--headless")  # or "--headless=new" if your Chrome supports it
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-backgrounding-occluded-windows")
    options.add_argument("--disable-renderer-backgrounding")

    # Set Chrome binary location explicitly to where chrome-stable installs on Debian-based systems
    options.binary_location = "/usr/bin/google-chrome-stable"

    service = Service()  # Selenium Manager auto-handles ChromeDriver

    driver = None
    try:
        driver = webdriver.Chrome(service=service, options=options)
        logging.info("Chrome WebDriver started")

        driver.get("https://uatwebland.ap.gov.in/weblanddashboard")
        wait = WebDriverWait(driver, 30)

        main_menu = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//a[contains(text(), '1. Abstract - Mutation For Corrections Reports')]")))
        driver.execute_script("arguments[0].scrollIntoView(true);", main_menu)
        ActionChains(driver).move_to_element(main_menu).pause(2).perform()

        mc4 = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//a[contains(text(), 'MC-4 :Sub-SLA Report on Mutation For Corrections')]")))
        driver.execute_script("arguments[0].scrollIntoView(true);", mc4)
        mc4.click()

        wg_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='పశ్చిమ గోదావరి']")))
        driver.execute_script("arguments[0].scrollIntoView(true);", wg_link)
        wg_link.click()

        narsapuram_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='నర్సాపురం']")))
        driver.execute_script("arguments[0].scrollIntoView(true);", narsapuram_link)
        narsapuram_link.click()

        logging.info("Selenium automation steps completed successfully.")

        time.sleep(10)

    except Exception as e:
        logging.error(f"Selenium error: {e}")

    finally:
        if driver:
            driver.quit()
            logging.info("Chrome WebDriver closed")

@app.route('/run-automation')
def run_automation():
    threading.Thread(target=run_selenium_script).start()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)
