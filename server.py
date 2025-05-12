from flask import Flask, request, send_file
import csv
import os
from datetime import datetime

app = Flask(__name__)

CSV_FILE = 'email_tracking_data.csv'

# Data storage dictionary (memory me temporarily rakhenge)
lead_data = {}

# Ensure CSV file has header if not exists
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            'Email ID', 'Sent Time', 
            'Email Opened (Yes/No)', 'First Opened At', 'Number of Opens',
            'Link Clicked (Yes/No)', 'First Clicked At', 'Number of Clicks',
            'Time to First Open (seconds)', 'Time to First Click (seconds)'
        ])

# Function to save/update the CSV
def save_to_csv():
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            'Email ID', 'Sent Time', 
            'Email Opened (Yes/No)', 'First Opened At', 'Number of Opens',
            'Link Clicked (Yes/No)', 'First Clicked At', 'Number of Clicks',
            'Time to First Open (seconds)', 'Time to First Click (seconds)'
        ])
        for email, data in lead_data.items():
            writer.writerow([
                email,
                data.get('sent_time', ''),
                'Yes' if data.get('opened_at') else 'No',
                data.get('opened_at', ''),
                data.get('num_opens', 0),
                'Yes' if data.get('clicked_at') else 'No',
                data.get('clicked_at', ''),
                data.get('num_clicks', 0),
                data.get('time_to_first_open', ''),
                data.get('time_to_first_click', '')
            ])

# API to record that email was sent
@app.route('/send_email')
def send_email():
    email = request.args.get('email')

    if email:
        sent_time = datetime.now()
        lead_data[email] = {
            'sent_time': sent_time.strftime('%Y-%m-%d %H:%M:%S'),
            'opened_at': None,
            'num_opens': 0,
            'clicked_at': None,
            'num_clicks': 0,
            'time_to_first_open': None,
            'time_to_first_click': None
        }
        save_to_csv()
        print(f"📧 Email Sent Logged: {email} at {sent_time}")
        return f"Email send record created for {email}"
    else:
        return "Missing email parameter!"

# API to track email open
@app.route('/track/open')
def track_open():
    email = request.args.get('email')

    if email and email in lead_data:
        now = datetime.now()
        if lead_data[email]['num_opens'] == 0:
            sent_time = datetime.strptime(lead_data[email]['sent_time'], '%Y-%m-%d %H:%M:%S')
            time_to_open = (now - sent_time).total_seconds()
            lead_data[email]['time_to_first_open'] = int(time_to_open)
            lead_data[email]['opened_at'] = now.strftime('%Y-%m-%d %H:%M:%S')
        
        lead_data[email]['num_opens'] += 1
        save_to_csv()
        print(f"✅ Email OPEN tracked: {email}")
    else:
        print(f"⚠️ Open tracking failed: email not found or missing parameter.")

    return send_file('pixel.png', mimetype='image/png')

# API to track link click
@app.route('/track/click')
def track_click():
    email = request.args.get('email')

    if email and email in lead_data:
        now = datetime.now()
        if lead_data[email]['num_clicks'] == 0:
            sent_time = datetime.strptime(lead_data[email]['sent_time'], '%Y-%m-%d %H:%M:%S')
            time_to_click = (now - sent_time).total_seconds()
            lead_data[email]['time_to_first_click'] = int(time_to_click)
            lead_data[email]['clicked_at'] = now.strftime('%Y-%m-%d %H:%M:%S')
        
        lead_data[email]['num_clicks'] += 1
        save_to_csv()
        print(f"✅ Link CLICK tracked: {email}")
    else:
        print(f"⚠️ Click tracking failed: email not found or missing parameter.")

    return "Click Tracked!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
