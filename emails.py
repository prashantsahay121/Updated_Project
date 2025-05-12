import pandas as pd
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException
from urllib.parse import urlparse, urlunparse

# 📂 Step 1: Load CSV
df = pd.read_csv("linkedin_companies_Information Technology_Ahmedabad.csv")
web_column = "Website"

# 🌐 Step 2: Clean URL (remove UTM and query params)
def clean_url(url):
    try:
        parsed = urlparse(url)
        return urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', '', '')).rstrip('/')
    except:
        return url

# 🔍 Step 3: Extract email from full rendered page
def get_email_with_selenium(driver, base_url):
    try:
        # Try multiple paths like /, /contact, /contact-us
        paths = ['', '/contact', '/contact-us', '/about']
        for path in paths:
            full_url = base_url + path
            print(f"🌐 Checking: {full_url}")
            driver.get(full_url)
            time.sleep(2)  # wait for JS to render

            page_text = driver.page_source
            emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", page_text)

            if emails:
                return emails[0]
        return "Not Available"
    except (TimeoutException, WebDriverException):
        return "Not Available"

# ⚙️ Step 4: Setup Selenium headless browser
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--log-level=3")  # suppress warnings

driver = webdriver.Chrome(options=options)

# 🧪 Step 5: Loop over URLs
results = []

for idx, url in enumerate(df[web_column]):
    print(f"\n🔎 [{idx+1}/{len(df)}] Scraping email from: {url}")
    if not isinstance(url, str) or not url.startswith("http"):
        results.append({"Website": url, "Email": "Not Available"})
        continue

    base_url = clean_url(url)
    email = get_email_with_selenium(driver, base_url)
    results.append({"Website": url, "Email": email})
    time.sleep(1)

driver.quit()

# 💾 Step 6: Save to CSV
email_df = pd.DataFrame(results)
email_df.to_csv("emails_with_selenium.csv", index=False)
print("\n✅ Emails saved to 'emails_with_selenium.csv'")
