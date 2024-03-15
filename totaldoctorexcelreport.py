from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import openpyxl

url = "https://health.hamropatro.com/doctors"
driver = webdriver.Chrome()
driver.get(url)

wb = openpyxl.Workbook()
ws = wb.active

ws.append(["Doctor Name"])

try:
    
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
            doctor_name = element.text
            ws.append([doctor_name])

        
        load_more_button = driver.find_elements(By.XPATH, "//button[contains(text(), 'Load More')]")
        if not load_more_button:
            break

except Exception as e:
    print("An error occurred while loading more doctors:", e)

finally:
    
    total_doctors = len(ws['A']) - 1  
    print(f"Total number of doctors: {total_doctors}")

    
    file_path = "doctor_report.xlsx"
    wb.save(file_path)
    print(f"Excel report saved successfully at: {file_path}")

    
    driver.quit()

