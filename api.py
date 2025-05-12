import requests
import pandas as pd

# Load Excel file
try:
    data = pd.read_excel('merged_data_output.xlsx')
    data.columns = data.columns.str.strip()  # remove extra spaces if any
    print("✅ Excel file loaded successfully.")
except Exception as e:
    print(f"❌ Error reading Excel file: {e}")
    exit()
# Loop through each row and send email request
for index, row in data.iterrows():
    receiver_email = str(row.get('Email')).strip()
    server_url = f"https://vpkfq3k0-5000.inc1.devtunnels.ms/send_email?email={receiver_email}"
    
    try:
        response = requests.get(server_url)
        if response.status_code == 200:
            print(f"✅ Email sent record created successfully for {receiver_email}")
        else:
            print(f"⚠️ Failed to record sent email for {receiver_email}")
    except Exception as e:
        print(f"❌ Error sending email to {receiver_email}: {e}")
