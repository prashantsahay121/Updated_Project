# merge_data.py

import pandas as pd

def merge_linkedin_and_email(linkedin_file, email_file, output_file="merged_data_output.xlsx"):
    try:
        df = pd.read_csv(linkedin_file)
        emails_df = pd.read_csv(email_file)

        if 'Email' not in emails_df.columns:
            raise ValueError("⚠️ 'Email' column not found in email file.")

        df['Email'] = emails_df['Email']
        df.to_excel(output_file, index=False)

        return df, output_file
    except Exception as e:
        raise RuntimeError(f"Error merging files: {e}")
