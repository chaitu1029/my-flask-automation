from flask import Flask, jsonify
from flask_cors import CORS
import threading
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import shutil
import pandas as pd

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin requests so your frontend can call this API

def run_webland_automation():
    USERNAME = "jcwg05999"
    PASSWORD = "Password#1"
    TARGET_DISTRICT = "పశ్చిమ గోదావరి-West Godavari"

    download_dir = os.path.join(os.getcwd(), "downloads")
    os.makedirs(download_dir, exist_ok=True)

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    options.add_experimental_option("prefs", prefs)

    # Use headless mode if running on server without GUI:
    # options.add_argument('--headless')
    # options.add_argument('--no-sandbox')
    # options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 20)

    def login_to_webland():
        driver.get("https://webland.ap.gov.in/")
        try:
            username = wait.until(EC.presence_of_element_located((By.ID, "useID")))
            username.clear()
            username.send_keys(USERNAME)

            password = driver.find_element(By.ID, "pqrabc")
            password.clear()
            password.send_keys(PASSWORD)

            Select(driver.find_element(By.ID, "ddlDist")).select_by_visible_text(TARGET_DISTRICT)
            driver.find_element(By.ID, "btnLogin").click()
            time.sleep(3)
            print("✅ Logged in successfully")
        except Exception as e:
            print("❌ Login failed:", e)

    def check_session_and_login():
        if "Session Logged Out" in driver.page_source or "Re-Login again" in driver.page_source:
            print("⚠️ Session expired, relogging...")
            login_to_webland()

    def click_exceptional_cases():
        try:
            wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Home"))).click()
            time.sleep(2)

            submenu_xpaths = [
                "//a[contains(text(), 'Exceptional Cases in Webland')]",
                "//a[contains(text(), 'Exceptional')]"
            ]
            submenu_item = None
            for xpath in submenu_xpaths:
                try:
                    submenu_item = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                    break
                except:
                    continue

            if submenu_item:
                driver.execute_script("arguments[0].scrollIntoView(true);", submenu_item)
                time.sleep(1)
                try:
                    submenu_item.click()
                except:
                    driver.execute_script("arguments[0].click();", submenu_item)
                print("✅ Navigated to Exceptional Cases")
            else:
                raise Exception("❌ Submenu not found")

        except Exception as e:
            print(f"❌ Navigation error: {e}")

    def process_all_mandals_and_villages():
        all_data = []

        mandal_dropdown = wait.until(EC.presence_of_element_located((By.ID, "MainContent_ddlmandal")))
        mandal_select = Select(mandal_dropdown)

        for mandal_index in range(1, len(mandal_select.options)):
            mandal_select = Select(wait.until(EC.presence_of_element_located((By.ID, "MainContent_ddlmandal"))))
            mandal_option = mandal_select.options[mandal_index]
            mandal_name = mandal_option.text.strip()
            mandal_code = mandal_option.get_attribute("value").strip()
            mandal_select.select_by_index(mandal_index)
            print(f"\n🔁 Mandal: {mandal_name} ({mandal_code})")
            time.sleep(2)

            try:
                village_dropdown = wait.until(EC.presence_of_element_located((By.ID, "MainContent_ddlvill")))
                village_select = Select(village_dropdown)

                for village_index in range(1, len(village_select.options)):
                    try:
                        village_dropdown = wait.until(EC.presence_of_element_located((By.ID, "MainContent_ddlvill")))
                        village_select = Select(village_dropdown)
                        village_option = village_select.options[village_index]
                        village_name = village_option.text.strip()
                        village_code = village_option.get_attribute("value").strip()
                        village_select.select_by_index(village_index)

                        print(f"   🏘️ Village: {village_name} ({village_code})")
                        time.sleep(1)

                        driver.switch_to.default_content()
                        try:
                            frame = wait.until(EC.presence_of_element_located((By.ID, "ifrm")))
                            driver.switch_to.frame(frame)
                        except:
                            pass

                        button_xpath = "//input[@type='submit' and contains(@value,'Get Details')]"
                        button = wait.until(EC.element_to_be_clickable((By.XPATH, button_xpath)))
                        driver.execute_script("arguments[0].scrollIntoView(true);", button)
                        time.sleep(0.5)
                        button.click()
                        time.sleep(2)

                        try:
                            export_xpath = "//input[contains(@value, 'Export') or contains(@title, 'Export')]"
                            export_button = WebDriverWait(driver, 5).until(
                                EC.element_to_be_clickable((By.XPATH, export_xpath))
                            )
                            driver.execute_script("arguments[0].scrollIntoView(true);", export_button)

                            before = set(os.listdir(download_dir))
                            export_button.click()
                            print("   📥 Export clicked... Waiting for download")

                            downloaded_file = None
                            for _ in range(20):
                                time.sleep(1)
                                after = set(os.listdir(download_dir))
                                new_files = after - before
                                new_files = [f for f in new_files if not f.endswith(".crdownload")]
                                if len(new_files) == 1:
                                    potential_file = os.path.join(download_dir, list(new_files)[0])
                                    if os.path.exists(potential_file):
                                        downloaded_file = potential_file
                                        break

                            if not downloaded_file:
                                raise Exception("❌ File download failed")

                            ext = os.path.splitext(downloaded_file)[1]
                            safe_mandal = mandal_name.replace("/", "_").replace("\\", "_")
                            safe_village = village_name.replace("/", "_").replace("\\", "_")
                            new_filename = f"{safe_mandal}_{safe_village}({village_code}){ext}"
                            new_path = os.path.join(download_dir, new_filename)
                            shutil.move(downloaded_file, new_path)
                            print(f"   ✅ File saved as: {new_filename}")
                            download_status = "Yes"

                        except:
                            print("   ❌ Export not available")
                            download_status = "No"

                        all_data.append({
                            "Mandal Name": mandal_name,
                            "Mandal Code": mandal_code,
                            "Village Name": village_name,
                            "Village Code": village_code,
                            "Downloaded": download_status
                        })

                    except Exception as e:
                        print(f"   ⚠️ Village Error: {e}")
                        continue

            except Exception as e:
                print(f"❌ Failed to load villages for Mandal {mandal_name}: {e}")
                continue

        if all_data:
            df = pd.DataFrame(all_data)
            status_path = os.path.join(download_dir, "All_Mandals_Village_Status.xlsx")
            df.to_excel(status_path, index=False)
            print(f"\n✅ Final status Excel saved: {status_path}")

    try:
        login_to_webland()
        check_session_and_login()
        click_exceptional_cases()
        process_all_mandals_and_villages()
    finally:
        driver.quit()

@app.route('/run_automation')
def run_automation_route():
    thread = threading.Thread(target=run_webland_automation)
    thread.start()
    return jsonify({"message": "Automation started in background. Check logs for progress."})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
