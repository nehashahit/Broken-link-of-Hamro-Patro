from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import requests

url = "https://jyotishsewa.alpha.hamrostack.com/"
driver = webdriver.Chrome()
driver.get(url)
wait = WebDriverWait(driver, 10)
links = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "a")))

print("Links:")
for link in links:
    url = link.get_attribute("href")
    if url:
        try:
            response = requests.head(url)
            status_code = response.status_code
            if status_code >= 400:
                print("Broken Link:", url, "Status Code:", status_code)
            else:
                print("Valid Link:", url, "Status Code:", status_code)
        except Exception as e:
            print("Exception while checking link:", url, "Error:", e)

image_links = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "img")))

print("Image Links:")
for image_link in image_links:
    try:
        src = image_link.get_attribute("src")
        if src and not src.startswith("data:image"):
            response = requests.head(src)
            status_code = response.status_code
            if status_code >= 400:
                print("Broken Image Link:", src, "Status Code:", status_code)
            else:
                print("Valid Image Link:", src, "Status Code:", status_code)
    except StaleElementReferenceException:
        
        image_links = driver.find_elements(By.TAG_NAME, "img")
        continue  
    except Exception as e:
        print("Exception while checking image link:", src, "Error:", e)

    image_links = driver.find_elements(By.TAG_NAME, "img")




driver.quit()
