import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

# --- 1. Load data ---
df = pd.read_csv('email_tracking_data.csv')
df.columns = df.columns.str.strip()

# --- 2. Feature Engineering ---
df['opened_flag'] = df['Email Opened (Yes/No)'].apply(lambda x: 1 if str(x).lower() == 'yes' else 0)
df['clicked_flag'] = df['Link Clicked (Yes/No)'].apply(lambda x: 1 if str(x).lower() == 'yes' else 0)

# Fill missing times with a large value to indicate "never opened/clicked"
df['Time to First Open (seconds)'] = df['Time to First Open (seconds)'].fillna(9999)
df['Time to First Click (seconds)'] = df['Time to First Click (seconds)'].fillna(9999)

# --- 3. Create target variable ---
if df['clicked_flag'].nunique() == 1:
    print(" Only one class found in clicked_flag. Adding synthetic cold samples...")
    cold_sample = df.sample(frac=0.3, random_state=42)
    df.loc[cold_sample.index, 'clicked_flag'] = 0

# --- 4. Define features and target ---
feature_columns = [
    'opened_flag', 'Number of Opens', 'Number of Clicks',
    'Time to First Open (seconds)', 'Time to First Click (seconds)'
]
X = df[feature_columns]
y = df['clicked_flag']

# --- 5. Train-Test Split ---
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# --- 6. Train Logistic Regression Model ---
model = LogisticRegression(max_iter=500)
model.fit(X_train, y_train)
print("\n Model training completed successfully!")

# --- 7. Predict and Evaluate ---
y_pred = model.predict(X_test)

print("\n Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\n Classification Report:")
print(classification_report(y_test, y_pred))
