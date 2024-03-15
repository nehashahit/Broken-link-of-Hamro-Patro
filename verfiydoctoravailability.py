from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import openpyxl

def check_doctors_availability(excel_file_path, website_url):
    driver = webdriver.Chrome()
    driver.get(website_url)

    try:
    
        wb = openpyxl.load_workbook(excel_file_path)
        ws = wb.active
        doctor_names_excel = set(cell.value for row in ws.iter_rows(min_row=2, min_col=1, max_col=1) for cell in row if cell.value)

        doctor_names_website = set()
        while True:
            load_more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Load More')]"))
            )
            driver.execute_script("arguments[0].scrollIntoView();", load_more_button)
            load_more_button.click()

            WebDriverWait(driver, 10).until(
                EC.invisibility_of_element_located((By.CLASS_NAME, "MuiCircularProgress-root"))
            )

            doctor_elements = driver.find_elements(By.CLASS_NAME, "MuiTypography-h5")
            for element in doctor_elements:
                doctor_names_website.add(element.text)

            load_more_button = driver.find_elements(By.XPATH, "//button[contains(text(), 'Load More')]")
            if not load_more_button:
                break

        missing_doctors = doctor_names_excel - doctor_names_website
        if missing_doctors:
            print("The following doctors are missing from the website:")
            for doctor in missing_doctors:
                print(doctor)
        else:
            print("All doctors from the Excel file are available on the website.")

    except Exception as e:
        print("An error occurred:", e)

    finally:
        driver.quit()
excel_file_path = "doctor_report.xlsx"
website_url = "https://health.hamropatro.com/doctors"
check_doctors_availability(excel_file_path, website_url)
