from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import requests
from datetime import datetime

url = "https://bank-rates.hamropatro.com/?utm_source=website&utm_medium=topmenubar&utm_campaign=target_investors"
driver = webdriver.Chrome()
driver.get(url)
wait = WebDriverWait(driver, 10)

current_url = driver.current_url

def get_status_message(status_code):
    if status_code < 200:
        return "Informational - " + str(status_code)
    elif status_code < 300:
        return "Success - " + str(status_code)
    elif status_code < 400:
        return "Redirection - " + str(status_code)
    elif status_code < 500:
        return "Client Error - " + str(status_code)
    else:
        return "Server Error - " + str(status_code)

links_by_status = {
    "Informational": [],
    "Success": [],
    "Redirection": [],
    "Client Error": [],
    "Server Error": []
}

links = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "a")))
print("Links:")
for link in links:
    try:
        url = link.get_attribute("href")
        if url:
            try:
                response = requests.head(url)
                status_code = response.status_code
                status_message = get_status_message(status_code)
                print(status_message + ": " + url)
                links_by_status[status_message.split(" - ")[0]].append((url, status_code))
            except Exception as e:
                print("Exception while checking link:", url, "Error:", e)
    except StaleElementReferenceException:
        continue

image_links = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "img")))
print("Image Links:")
for image_link in image_links:
    try:
        src = image_link.get_attribute("src")
        if src and not src.startswith("data:image"):
            response = requests.head(src)
            status_code = response.status_code
            status_message = get_status_message(status_code)
            print(status_message + ": " + src)
            links_by_status[status_message.split(" - ")[0]].append((src, status_code))
    except StaleElementReferenceException:
        continue
    except Exception as e:
        print("Exception while checking image link:", src, "Error:", e)

driver.quit()

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

total_links_by_status = {status: len(links_info) for status, links_info in links_by_status.items()}

total_links_html = """
<table style="width: 30%; margin-bottom: 20px;">
    <tr class="title-row" style="background-color: #007bff; color: white;">
        <th style="background-color: #007bff;">Status Code</th>
        <th style="background-color: #007bff;">Total Links</th>
    </tr>
"""

for status, count in total_links_by_status.items():
    status_code = status.split(' - ')[-1]
    if status_code.isdigit():
        status_code = int(status_code)
        if status_code < 200:
            status_range = "< 200"
        elif status_code < 300:
            status_range = "< 300"
        elif status_code < 400:
            status_range = "< 400"
        elif status_code < 500:
            status_range = "< 500"
        else:
            status_range = ">= 500"
        status_code = status_range
    total_links_html += f"""
    <tr>
        <td>{status_code}</td>
        <td>{count}</td>
    </tr>
"""
total_links_html += "</table>"


links_table_html = """
<table style="width: 50%;">
    <tr class="title-row" style="background-color: #007bff; color: white;">
        <th style="background-color: #007bff;">URL</th>
        <th style="background-color: #007bff;">Status</th>
        <th style="background-color: #007bff;">Broken Link</th>
    </tr>
"""
for status, links_info in links_by_status.items():
    total_links = len(links_info)
    if total_links > 0:
        for link_info in links_info:
            url = link_info[0]
            status_code = link_info[1]
            broken_link = "Yes" if status_code >= 400 else "No"
            links_table_html += f"""
                <tr>
                    <td style="width: 50%;"><a href='{url}'>{url}</a></td>
                    <td style="width: 20%;">{status_code}</td>
                    <td style="width: 30%;">{broken_link}</td>
                </tr>
            """
links_table_html += "</table>"

# Generate the final HTML report
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
        }}
        th, td {{
            border: 1px solid #dddddd;
            text-align: left;
            padding: 8px;
        }}
        th {{
            background-color: #f2f2f2;
        }}
        .title-row th {{
            background-color: #007bff;
            color: white;
            padding: 8px;
        }}
    </style>
</head>
<body>
    <h1>Links Summary</h1>
    <p>Website URL: <a href="{current_url}">{current_url}</a></p>
    <p>Total Links by Status:</p>
    {total_links_html}
    <h1>Individual Links Report</h1>
    <p>Timestamp: {timestamp}</p>
    {links_table_html}
</body>
</html>
"""

with open("bankrate_links_report.html", "w") as file:
    file.write(report_html)

print("HTML report generated successfully!")
