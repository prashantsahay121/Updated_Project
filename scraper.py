# scraper.py

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv

USERNAME = "prashantsahay121@gmail.com"
PASSWORD = ""

def login_to_linkedin(driver):
    driver.get("https://www.linkedin.com/login")
    time.sleep(2)
    driver.find_element(By.ID, "username").send_keys(USERNAME)
    driver.find_element(By.ID, "password").send_keys(PASSWORD)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(5)

def extract_about_details(driver):
    details = {
        "Industry": "N/A",
        "Website": "N/A",
        "Phone": "N/A",
        "Company size": "N/A",
        "Specialties": "N/A"
    }
    try:
        dts = driver.find_elements(By.XPATH, "//dl[contains(@class, 'overflow-hidden')]//dt")
        dds = driver.find_elements(By.XPATH, "//dl[contains(@class, 'overflow-hidden')]//dd")
        for dt, dd in zip(dts, dds):
            label = dt.text.strip()
            value = dd.text.strip()
            if label in details:
                if label == "Phone":
                    value = value.replace("Phone number is", "").strip().strip('"').strip(',')
                details[label] = value
    except Exception as e:
        print("❌ Error extracting about details:", e)
    return details

def scrape_linkedin_companies(url, category, city):
    driver = webdriver.Chrome()
    login_to_linkedin(driver)

    company_details = []
    visited_links = set()
    phone_numbers_seen = set()

    for page in range(1, 6):
        search_url = f"{url}&page={page}"
        driver.get(search_url)
        time.sleep(5)

        for _ in range(3):
            driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
            time.sleep(2)

        elements = driver.find_elements(By.XPATH, '//a[contains(@href, "/company/")]')
        links = []
        for el in elements:
            href = el.get_attribute("href")
            if href and "/company/" in href and href not in visited_links:
                visited_links.add(href)
                links.append(href.split("?")[0])

        for link in links:
            try:
                driver.get(link + "about/")
                time.sleep(3)
                company_name = driver.find_element(By.TAG_NAME, "h1").text.strip()
                about = extract_about_details(driver)

                phone = about["Phone"]
                if phone != "N/A" and phone in phone_numbers_seen:
                    continue
                if phone != "N/A":
                    phone_numbers_seen.add(phone)

                company_details.append([
                    company_name,
                    about["Industry"],
                    about["Website"],
                    about["Phone"],
                    about["Company size"],
                    about["Specialties"],
                    city
                ])
            except Exception:
                continue

    with open(f"linkedin_companies_{category}_{city}.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Company Name", "Industry", "Website", "Phone", "Company Size", "Specialties", "Location"])
        for row in company_details:
            clean_row = [str(col).replace('\n', ' ').replace('"', '').strip() for col in row]
            writer.writerow(clean_row)

    driver.quit()
    return len(company_details)
