from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import requests
from datetime import datetime

url = "https://pay.hamropatro.com/"

try:
    driver = webdriver.Chrome()
    driver.get(url)
    wait = WebDriverWait(driver, 30)  # Increased timeout to 30 seconds

    print("WebDriver initialized successfully.")
    print("Waiting for anchor elements...")
    links = wait.until(EC.visibility_of_all_elements_located((By.TAG_NAME, "a")))
    print(f"Found {len(links)} anchor elements.")
    print("Checking anchor elements...")

    for link in links:
        try:
            href = link.get_attribute("href")
            if href:
                print(f"Checking link: {href}")
                response = requests.head(href)
                status_code = response.status_code
                print(f"Status code for {href}: {status_code}")
        except Exception as e:
            print(f"Error while checking link: {href}, Error: {e}")

    print("Anchor element check completed.")

    print("Waiting for image elements...")
    image_links = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "img")))
    print(f"Found {len(image_links)} image elements.")
    print("Checking image elements...")

    for image_link in image_links:
        try:
            src = image_link.get_attribute("src")
            if src and not src.startswith("data:image"):
                print(f"Checking image src: {src}")
                response = requests.head(src)
                status_code = response.status_code
                print(f"Status code for {src}: {status_code}")
        except Exception as e:
            print(f"Error while checking image link: {src}, Error: {e}")

    print("Image element check completed.")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("Generating HTML report...")

    report_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Links Report</title>
        <style>
            table {{
                border-collapse: collapse;
                width: 100%;
            }}
            th, td {{
                border: 1px solid #dddddd;
                text-align: left;
                padding: 8px;
            }}
            th {{
                background-color: #f2f2f2;
            }}
        </style>
    </head>
    <body>
        <h1>Links Report</h1>
        <p>Website URL: <a href="{url}">{url}</a></p>
        <p>Timestamp: {timestamp}</p>
        <table>
            <tr>
                <th>URL</th>
                <th>Status</th>
                <th>Broken Link</th>
            </tr>
    """

    # Generate HTML report

    report_html += """
        </table>
    </body>
    </html>
    """

    with open("hamropay_links_report.html", "w") as file:
        file.write(report_html)

    print("HTML report generated successfully!")

except TimeoutException as te:
    print("Timeout occurred while waiting for elements:", te)

except Exception as e:
    print("An error occurred:", e)

finally:
    driver.quit()
