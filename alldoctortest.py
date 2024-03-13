
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()

def verify_name():
    driver.implicitly_wait(20)
    driver.get("https://health.hamropatro.com/doctors")
    driver.title
    driver.maximize_window()

    time.sleep(5)
    wait = WebDriverWait(driver, 20)
    element = wait.until(EC.element_to_be_clickable((By.ID, "search-input")))
    element.send_keys("Imran Ansari")
    element.send_keys(Keys.ENTER)

    expected_result = "Dr. Imran Ansari"
    print("Expected Result:", expected_result)
    actual_result = driver.find_element(By.XPATH, "//*[@id=\"root\"]/div/div/div[2]/div[3]/div/div/div/div/div[2]/div/h5").text
    assert actual_result == expected_result, "Book name not matched"
    print("Actual Result:", actual_result)
    time.sleep(5)
    driver.close()

if __name__ == "__main__":
    verify_name()