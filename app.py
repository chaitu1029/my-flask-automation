import threading
import logging
from flask import Flask, redirect, url_for
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

def run_selenium():
    logging.info("Selenium automation started")
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        # Chrome binary installed in the container
        options.binary_location = "/usr/bin/google-chrome"

        # ChromeDriver binary installed in the container
        service = Service(executable_path="/usr/local/bin/chromedriver")

        driver = webdriver.Chrome(service=service, options=options)
        driver.get("https://example.com")
        logging.info(f"Page title: {driver.title}")
        driver.quit()
        logging.info("Selenium automation finished successfully")
    except Exception as e:
        logging.error(f"Selenium error: {e}")

@app.route('/run-automation')
def run_automation():
    threading.Thread(target=run_selenium).start()
    return redirect(url_for('index'))

@app.route('/')
def index():
    return "Selenium automation started - check logs"

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
