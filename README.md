# 📩 Automated Email Campaign & Lead Scoring System

## Overview

This project is a **full pipeline** that:

- Scrapes company data from LinkedIn.
- Merges it with email information.
- Sends personalized marketing emails.
- Tracks user engagement (email opens, clicks).
- Predicts Hot/Cold leads using Machine Learning.
- Generates a final campaign performance report.

---

## ✨ Features

- **Company Scraping**: Fetches company details (industry, website, phone, etc.) from LinkedIn using Selenium.
- **Email Sending**: Sends personalized HTML emails using Gmail SMTP and tracks opens and clicks.
- **Engagement Tracking**: Flask server APIs log email sent, opens (pixel tracking), and link clicks.
- **Lead Scoring Model**: Trains a Logistic Regression model to predict Hot and Cold leads based on engagement.
- **Campaign Analytics**: Summarizes Open Rate, Click-Through Rate, Hot Leads, and Cold Leads.

---

## 💂️ Project Structure

| File                     | Description                                                                                        |
| ------------------------ | -------------------------------------------------------------------------------------------------- |
| `scrape_linkedin.py`     | Scrapes LinkedIn company profiles and saves to  `linkedin_company_about_details.csv`              |
| `emails.py`              | Merges company data with emails into `updated_data_file.xlsx`.                                     |
| `emaills.py`             | Sends personalized HTML emails and tracks records.                                                 |
| `email_template.html`    | Responsive, dynamic email template with open & click tracking.                                     |
| `server2.py`             | Flask server to track email opens and link clicks, and record data into `email_tracking_data.csv`. |
| `api.py`                 | Alternative script to hit the `/send_email` endpoint for logging sent emails.                      |
| `automation_hitemail.py` | Automates hitting open and click tracking URLs using Selenium.                                     |
| `ML_Model.py`            | Trains a Machine Learning model to classify leads as Hot or Cold based on tracking behavior.       |
| `Report.py`              | Generates final analytics and saves campaign summary report.                                       |

---

## ⚙️ Setup Instructions

### 1. Install Requirements

```bash
pip install pandas scikit-learn flask selenium webdriver-manager openpyxl
```

### 2. Scrape Company Data

- Open `scrape_linkedin.py`.
- Ensure you have updated your LinkedIn credentials.
- Run the script:

```bash
python scrape_linkedin.py
```

### 3. Merge Emails

- Place your `emails.csv` file alongside the scripts.
- Run:

```bash
python emails.py
```

- It will generate `updated_data_file.xlsx`.

### 4. Start Tracking Server

- Run:

```bash
python server2.py
```

- This will start the Flask server on port 5000 for email tracking.

### 5. Send Emails

- Configure sender details in `emaills.py`.
- Run:

```bash
python emaills.py
```

### 6. (Optional) Automate Tracking Verification

- Run:

```bash
python automation_hitemail.py
```

### 7. Train the ML Model

- Run:

```bash
python ML_Model.py
```

### 8. Generate Campaign Report

- Run:

```bash
python Report.py
```

---

## 📊 Output Files

- `linkedin_company_about_details.csv`: Scraped LinkedIn company data.
- `updated_data_file.xlsx`: Merged company + email data.
- `email_tracking_data.csv`: Engagement tracking data (opens, clicks).
- `Lead_Scoring_Report.csv`: Predicted lead status after ML model.
- `Campaign_Analytics_Summary.csv`: Final performance summary.

---

## 🔥 Highlights

- **Real Email Tracking** using a tracking pixel and link tracking.
- **Machine Learning Integration** for smarter lead classification.
- **Automated Scraping** and **Automated Campaign Execution**.
- **Beautiful HTML Emails** personalized for each receiver.

---

## 🚀 Future Enhancements

- Add real unsubscribe link handling.
- Integrate with CRM systems like HubSpot or Salesforce.
- Enhance ML model with more features like email response time, bounce rates, etc.

---

## 🧑‍💻 Author

**Prashant Sahay**\
[Business Development Manager @ Tech Innovators Inc.]

