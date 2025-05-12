import pandas as pd

# 1. Load the data
data = pd.read_csv('email_tracking_data.csv')

# 2. Preprocessing
data['Email Opened (Yes/No)'] = data['Email Opened (Yes/No)'].map({'Yes': 1, 'No': 0})
data['Link Clicked (Yes/No)'] = data['Link Clicked (Yes/No)'].map({'Yes': 1, 'No': 0})

# Replace NaN with 0 in numerical fields
data[['Number of Opens', 'Time to First Open (seconds)']] = data[['Number of Opens', 'Time to First Open (seconds)']].fillna(0)

# Optional: Include these only if present
if 'Number of Clicks' not in data.columns:
    data['Number of Clicks'] = 0

if 'Time on Page (seconds)' not in data.columns:
    data['Time on Page (seconds)'] = 0

# 3. Calculate Score
data['Score'] = (
    (data['Email Opened (Yes/No)'] == 1).astype(int) +
    (data['Number of Opens'] > 2).astype(int) +
    (data['Link Clicked (Yes/No)'] == 1).astype(int) +
    (data['Time to First Open (seconds)'] < 60).astype(int) +
    (data['Number of Clicks'] > 1).astype(int) +
    (data['Time on Page (seconds)'] > 30).astype(int)
)

# 4. Lead Classification
data['Lead Status (Predicted)'] = data['Score'].apply(lambda x: 'Hot Lead' if x >= 3 else 'Cold Lead')

# 5. Create and Save Report
report = data[['Email ID', 'Number of Opens', 'Time to First Open (seconds)', 'Lead Status (Predicted)']]
report.to_csv('Advanced_Lead_Scoring_Report.csv', index=False)
print("Advanced Lead Scoring Report generated successfully: 'Advanced_Lead_Scoring_Report.csv'")
