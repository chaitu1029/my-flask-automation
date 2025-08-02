from flask import Flask, render_template, redirect, url_for
import threading

app = Flask(__name__)

@app.route('/run-python-code')
def run_python_code():
    return render_template('index.html')

def run_selenium_script():
    # Insert your Selenium code here (from your test3.py)
    from selenium import webdriver
    from selenium.webdriver.edge.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import time

    EDGE_DRIVER_PATH = r"C:\Users\chait\Documents\fuzzy_match\edgedriver\msedgedriver.exe"
    service = Service(EDGE_DRIVER_PATH)
    driver = webdriver.Edge(service=service)
    driver.maximize_window()
    driver.get("https://uatwebland.ap.gov.in/weblanddashboard")
    wait = WebDriverWait(driver, 30)

    try:
        main_menu = wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(), '1. Abstract - Mutation For Corrections Reports')]")))
        driver.execute_script("arguments[0].scrollIntoView(true);", main_menu)
        ActionChains(driver).move_to_element(main_menu).pause(2).perform()

        mc4 = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'MC-4 :Sub-SLA Report on Mutation For Corrections')]")))
        driver.execute_script("arguments[0].scrollIntoView(true);", mc4)
        mc4.click()

        wg_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='పశ్చిమ గోదావరి']")))
        driver.execute_script("arguments[0].scrollIntoView(true);", wg_link)
        wg_link.click()

        narsapuram_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='నర్సాపురం']")))
        driver.execute_script("arguments[0].scrollIntoView(true);", narsapuram_link)
        narsapuram_link.click()

    except Exception as e:
        print("[❌] Error occurred:", e)
    time.sleep(10)
    driver.quit()

@app.route('/run-automation')
def run_automation():
    # Run selenium script in a background thread to avoid blocking Flask requests
    threading.Thread(target=run_selenium_script).start()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
