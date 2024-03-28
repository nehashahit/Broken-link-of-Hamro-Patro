import time
import traceback  
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
import openpyxl

wb = openpyxl.load_workbook("doctor_report.xlsx")
sheet = wb.active

doctor_names = [cell.value for cell in sheet['A'][1:] if cell.value]

output_wb = openpyxl.Workbook()
output_sheet = output_wb.active
output_sheet.append(["Doctor Name", "NMC_no", "Designation", "Specialities", "Price"])

driver = webdriver.Chrome()
driver.get("https://health.hamropatro.com/doctors")

try:
    for doctor_name in doctor_names:
        search_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "search-input"))
        )
        search_input.clear()
        search_input.send_keys(doctor_name)
        time.sleep(5)  
        search_input.send_keys(Keys.ENTER)

        time.sleep(5)  

        try:
            doctor_profile_links = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "MuiCard-root") and contains(@class, "consultant-profile-card")][.//h5[contains(text(), "' + doctor_name + '")]]'))
            )

            for i in range(len(doctor_profile_links)):
                try:
                    doctor_profile_links = WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "MuiCard-root") and contains(@class, "consultant-profile-card")][.//h5[contains(text(), "' + doctor_name + '")]]'))
                    )
                    doctor_profile_links[i].click()
                    time.sleep(3)

                    doctor_info = [doctor_name]

                    try:
                        nmc_no_element = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/div[2]/div/div[2]/div[1]/div[1]/div[3]/h5')
                        nmc_no = nmc_no_element.text.strip()
                    except NoSuchElementException:
                        nmc_no = "N/A"
                    doctor_info.append(nmc_no)

                    try:
                        designation_element = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/div[2]/div/div[2]/div[1]/div[1]/div[3]/p[2]')
                        designation = designation_element.text.strip()
                    except NoSuchElementException:
                        designation = "N/A"
                    doctor_info.append(designation)

                    try:
                        specialities_element = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/div[2]/div/div[2]/div[1]/div[1]/div[4]/div/span')
                        specialities = specialities_element.text.strip()
                    except NoSuchElementException:
                        specialities = "N/A"
                    doctor_info.append(specialities)

                    try:
                        price_element = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/div[2]/div/div[2]/div[1]/div[2]/div/div')
                        price = price_element.text.strip()
                    except NoSuchElementException:
                        price = "N/A"
                    doctor_info.append(price)
                    
                    output_sheet.append(doctor_info)

                except StaleElementReferenceException:
                    print("Search input reference is stale. Re-locating the search input.")
                    search_input = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.ID, "search-input"))
                    )
                    search_input.clear()
                    break

                except Exception as e:
                    print(f"Error processing doctor profile for {doctor_name}: {e}")
                    traceback.print_exc()  
                finally:
                    driver.back()
                    time.sleep(3)

                    search_input = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.ID, "search-input"))
                    )

        except Exception as e:
            print(f"No doctor profiles found for {doctor_name}: {e}")

        for _ in range(len(doctor_name)):
            search_input.send_keys(Keys.BACKSPACE)

finally:
    output_wb.save("doctor_information1.xlsx")
    driver.quit()

    

