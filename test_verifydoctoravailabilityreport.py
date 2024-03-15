import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import openpyxl

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def read_doctor_names(file_path):
    try:
        wb = openpyxl.load_workbook(file_path)
        sheet = wb.active

        doctor_names = [cell.value for cell in sheet['A'][1:] if cell.value]
        print("Doctor names from Excel file:", doctor_names)
        return doctor_names
    except FileNotFoundError as e:
        print("Excel file not found:", e)
        return []
    except Exception as e:
        print("An error occurred while reading the Excel file:", e)
        return []

@pytest.mark.parametrize("doctor_name", read_doctor_names("doctor_report.xlsx"))
def test_doctor_availability(driver, doctor_name):
    website_url = "https://health.hamropatro.com/doctors"

    try:
        print(f"Searching for doctor: {doctor_name}")

        driver.get(website_url)

        search_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "search-input")))
        search_input.clear()
        search_input.send_keys(doctor_name)
        search_input.send_keys(Keys.ENTER)

        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "MuiTypography-h5")))

        doctor_profile = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='root']/div/div/div[2]/div[3]/div/div/div/div/div[2]/div/h5"))).text

        assert doctor_name in doctor_profile, f"{doctor_name} not found in search results"

        print(f"Doctor {doctor_name} found.")

    except Exception as e:
        print(f"An error occurred for {doctor_name}: {e}")
        raise

if __name__ == "__main__":
    pytest.main(["-v", "--html=report.html"])

    print("Report generated successfully. You can find it at: report.html")
