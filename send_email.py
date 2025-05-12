import sys
import pandas as pd
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

# Sender configuration constants
YOUR_EMAIL = 'techtesting524@gmail.com'
YOUR_PASSWORD = 'unzoqjpzdrahdmtd'  # Gmail App Password
YOUR_NAME = 'Prashant Sahay'
YOUR_POSITION = 'Business Development Manager'
YOUR_COMPANY_NAME = 'Tech Innovators Inc.'
YOUR_CONTACT_EMAIL = 'prashant@techinnovators.com'
YOUR_LOCATION = 'New Delhi, India'

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587


def send_emails(excel_path: str):
    """
    Reads recipient data from the given Excel file and sends emails accordingly.
    """
    # 1. Read the Excel file
    try:
        data = pd.read_excel(excel_path)
        data.columns = data.columns.str.strip()
        print(f"[SUCCESS] Excel file '{excel_path}' loaded successfully.")
    except Exception as e:
        print(f"[ERROR] Error reading Excel file '{excel_path}': {e}")
        return

    # 2. Load HTML Template
    try:
        with open('email_template.html', 'r', encoding='utf-8') as file:
            html_template = file.read()
        print("[SUCCESS] Email template loaded successfully.")
    except Exception as e:
        print(f"[ERROR] Error reading HTML template: {e}")
        return

    # 3. Setup SMTP server
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(YOUR_EMAIL, YOUR_PASSWORD)
        print("[SUCCESS] SMTP Server login successful.")
    except Exception as e:
        print(f"[ERROR] SMTP Server connection failed: {e}")
        return

    # 4. Iterate and send
    for index, row in data.iterrows():
        try:
            company = str(row.get('Company Name', 'Valued Company')).strip()
            industry = str(row.get('Industry', 'Technology')).strip()
            website = str(row.get('Website', '#')).strip()
            receiver_email = str(row.get('Email')).strip()

            # Construct tracking URLs
            open_tracking_url = f"https://vpkfq3k0-5000.inc1.devtunnels.ms/track/open?email={receiver_email}"
            click_tracking_url = f"https://vpkfq3k0-5000.inc1.devtunnels.ms/track/click?email={receiver_email}"
            server_url = f"https://vpkfq3k0-5000.inc1.devtunnels.ms/send_email?email={receiver_email}"

            # Record email in backend
            try:
                response = requests.get(server_url)
                if response.status_code == 200:
                    print(f"[SUCCESS] Email record logged for {receiver_email}")
                else:
                    print(f"[WARNING] Logging failed for {receiver_email} (status {response.status_code})")
            except Exception as e:
                print(f"[ERROR] Error logging email for {receiver_email}: {e}")

            # Prepare HTML and plain text bodies
            email_html = (
                html_template
                .replace('[Company Name]', company)
                .replace('[Industry]', industry)
                .replace('[Website]', website)
                .replace('[Your Name]', YOUR_NAME)
                .replace('[Your Position]', YOUR_POSITION)
                .replace('[Your Company Name]', YOUR_COMPANY_NAME)
                .replace('[Your Contact Email]', YOUR_CONTACT_EMAIL)
                .replace('[Email]', receiver_email)
                .replace('[Location]', YOUR_LOCATION)
                .replace('[CTA Link]', website)
                .replace('[Open Tracking URL]', open_tracking_url)
                .replace('[Click Tracking URL]', click_tracking_url)
            )

            plain_text = f"""Dear {company} Team,

I hope you're doing well. I recently learned about your impressive work in the {industry} sector and wanted to reach out regarding a potential collaboration.

At {YOUR_COMPANY_NAME}, we help businesses like yours streamline operations and accelerate digital growth with tailored solutions.

If you're open to a conversation, I'd be happy to set up a quick call at your convenience. Feel free to explore more about us here: {website}

Looking forward to hearing from you.

Best regards,
{YOUR_NAME}
{YOUR_POSITION}
{YOUR_COMPANY_NAME}
{YOUR_CONTACT_EMAIL}
"""

            # Create email message
            msg = MIMEMultipart('alternative')
            msg['From'] = formataddr((YOUR_NAME, YOUR_EMAIL))
            msg['To'] = receiver_email
            msg['Subject'] = f"Exploring Digital Growth Opportunities with {company}"
            msg.attach(MIMEText(plain_text, 'plain'))
            msg.attach(MIMEText(email_html, 'html'))

            # Send the email
            server.sendmail(YOUR_EMAIL, receiver_email, msg.as_string())
            print(f"[SUCCESS] Email sent successfully to {receiver_email}")

        except Exception as e:
            print(f"[ERROR] Error sending email to {receiver_email}: {e}")

    # 5. Quit the server
    try:
        server.quit()
        print("[SUCCESS] SMTP server connection closed.")
    except Exception as e:
        print(f"[WARNING] Error closing SMTP server: {e}")


if __name__ == "__main__":
    excel_path = sys.argv[1] if len(sys.argv) > 1 else 'merged_data_output.xlsx'
    send_emails(excel_path)
