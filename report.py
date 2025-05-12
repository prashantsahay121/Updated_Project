import pandas as pd

# 1. Load the tracking data
tracking_data = pd.read_csv('email_tracking_data.csv')

# 2. Load the lead scoring report
lead_report = pd.read_csv('Advanced_Lead_Scoring_Report.csv')

# 3. Calculate Metrics

# Number of emails sent
num_emails_sent = tracking_data.shape[0]

# Open Rate = (Number of Opened Emails / Total Emails) * 100
num_opens = tracking_data['Email Opened (Yes/No)'].map({'Yes': 1, 'No': 0}).sum()
open_rate = (num_opens / num_emails_sent) * 100

# Click-through Rate = (Number of Clicked Emails / Total Emails) * 100
num_clicks = tracking_data['Link Clicked (Yes/No)'].map({'Yes': 1, 'No': 0}).sum()
click_through_rate = (num_clicks / num_emails_sent) * 100

# Number of Hot Leads and Cold Leads
num_hot_leads = (lead_report['Lead Status (Predicted)'] == 'Hot Lead').sum()
num_cold_leads = (lead_report['Lead Status (Predicted)'] == 'Cold Lead').sum()

# 4. Print the Final Report
print(" Final Campaign Analytics Report:")
print("-------------------------------------")
print(f" Number of Emails Sent: {num_emails_sent}")
print(f" Open Rate: {open_rate:.2f}%")
print(f" Click-Through Rate: {click_through_rate:.2f}%")
print(f" Number of Hot Leads: {num_hot_leads}")
print(f" Number of Cold Leads: {num_cold_leads}")

# 5. Optionally Save this as a CSV/Excel File
report_summary = {
    'Metric': ['Number of Emails Sent', 'Open Rate (%)', 'Click-Through Rate (%)', 'Number of Hot Leads', 'Number of Cold Leads'],
    'Value': [num_emails_sent, round(open_rate, 2), round(click_through_rate, 2), num_hot_leads, num_cold_leads]
}

summary_df = pd.DataFrame(report_summary)
summary_df.to_csv('Campaign_Analytics_Summary.csv', index=False)
print("\n Campaign Analytics Summary saved as 'Campaign_Analytics_Summary.csv'.")
