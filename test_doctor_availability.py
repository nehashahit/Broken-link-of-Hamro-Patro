import openpyxl
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def read_doctor_names(file_path):
    wb = openpyxl.load_workbook(file_path)
    sheet = wb.active
    return [cell.value for cell in sheet['A'][1:] if cell.value]

def test_search_single_doctor():
    excel_file_path = "doctor_report.xlsx"
    
    doctor_names = read_doctor_names(excel_file_path)
    
    doctor_name = doctor_names[0]

    driver = webdriver.Chrome()
    driver.get("https://health.hamropatro.com/doctors")
    
    try:
        # Find search input element and enter doctor's name
        search_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "search-input")))
        search_input.clear()
        search_input.send_keys(doctor_name)
        search_input.send_keys(Keys.ENTER)
        expectedResult= doctor_name[0]

        actualResult= WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "MuiTypography-h5"))).get_attribute

        doctor_profile = driver.find_elements(By.XPATH, f"//h5[contains(text(), '{doctor_name}')]")
    
        assert doctor_profile, f"{doctor_name} not found in search results"

    finally:
    
        driver.quit()

if __name__ == "__main__":
    pytest.main()
