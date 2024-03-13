import openpyxl
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Function to read doctor's names from Excel report
def read_doctor_names(file_path):
    wb = openpyxl.load_workbook(file_path)
    sheet = wb.active
    return [cell.value for cell in sheet['A'][1:] if cell.value]

# Test function to search for doctors and assert the search results
def test_search_doctors():
    # Excel file path
    excel_file_path = "doctor_report.xlsx"
    
    # Load doctor's names from Excel report
    doctor_names = read_doctor_names(excel_file_path)
    
    # Open Chrome browser
    driver = webdriver.Chrome()
    driver.get("https://health.hamropatro.com/doctors")
    
    try:
        for doctor_name in doctor_names:
            # Find search input element and enter doctor's name
            search_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "search-input")))
            search_input.clear()
            search_input.send_keys(doctor_name)
            search_input.send_keys(Keys.ENTER)
        
            # Wait for search results to load
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "MuiTypography-h5")))

            # Find doctor's profile on search results page
            doctor_profile = driver.find_elements(By.XPATH, f"//h5[contains(text(), '{doctor_name}')]")
        
            # Assert that the doctor's profile is found
            assert doctor_profile, f"{doctor_name} not found in search results"
        
            # Wait for a specified amount of time (adjust as needed)
            time.sleep(3)  # Wait for 3 seconds
        
            # Clear search box by sending backspace keys
            for _ in range(len(doctor_name)):
                search_input.send_keys(Keys.BACKSPACE)
        
    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    pytest.main()
