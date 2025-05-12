import streamlit as st
import pandas as pd
import os
import re
import time
import requests
import subprocess
from io import BytesIO
from scraper import scrape_linkedin_companies
import base64

# --- STATIC DATA ---
cities = {
    "Ahmedabad": "104990346",
    "Hyderabad": "105556991",
    "Indore": "101389470",
    "Pune": "103671728"
}

domains = [
    "Information Technology",
    "Artificial Intelligence",
    "Machine Learning",
    "Data Science",
    "Software as a Service"
]

industries = [
    "Professional Services",
    "IT Services and IT Consulting",
    "Technology, Information and Media",
    "Technology, Information and Internet",
    "Software Development"
]

base_url = (
    "https://www.linkedin.com/search/results/companies/"
    "?companyHqGeo=%5B%22{geo_code}%22%5D&keywords={keyword}"
)
linkedin_url_map = {
    domain: {
        city: base_url.format(
            geo_code=geo_code,
            keyword=domain.replace(" ", "%20")
        )
        for city, geo_code in cities.items()
    }
    for domain in domains
}


# --- STREAMLIT CONFIGURATION ---
st.set_page_config(page_title="Multi-Tool Scraper & Email Sender", layout="wide")
st.title("🔍 Multi-Tool Scraper & Email Sender")



# --- Set Background Image from Local File ---
def set_bg_image_local(image_path):
    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg_image_local("back.png")


# Sidebar operation selector
operation = st.sidebar.selectbox(
    "Select Operation",
    [
        "ICP Scrape",
        "Email Scrape",
        "Merge Data",
        "Email Template Viewer",
        "Send Email",
        "Live Tracking",
        "Evaluate Model",
        "Advanced Lead Scoring",
        "Campaign Report Summary",
        "Create Jira Tasks",
        "Create GitHub Repo from Tasks",
        "Generate Test Cases"
    ]
)

# Display last LinkedIn data if available
if "linkedin_data" in st.session_state and "linkedin_filename" in st.session_state:
    with st.sidebar:
        st.markdown("### 📁 Last LinkedIn Scrape")
        st.write(f"`{st.session_state.linkedin_filename}`")
        st.dataframe(st.session_state.linkedin_data)

# --- ICP SCRAPE MODE ---
if operation == "ICP Scrape":
    st.header("Ideal Customer Profile Scraper")
    category = st.selectbox("Select Domain", domains)
    city = st.selectbox("Select City", list(cities.keys()))

    st.text_input("Category", value="Company", disabled=True)
    st.markdown("### Industry (Fixed)")
    for ind in industries:
        st.checkbox(ind, value=True, disabled=True)

    if st.button("Start ICP Scraping"):
        url = linkedin_url_map[category][city]
        st.write(f"Scraping **{category}** companies in **{city}**...")
        try:
            count = scrape_linkedin_companies(url, category, city)
            filename = f"linkedin_companies_{category}_{city}.csv"
            if os.path.exists(filename):
                df = pd.read_csv(filename)
                st.session_state.linkedin_data = df
                st.session_state.linkedin_filename = filename
                with st.sidebar:
                    st.markdown("### 📂 Scrape Output")
                    st.write(f"`{filename}`")
                    st.dataframe(df)
                    st.download_button(
                        "⬇️ Download CSV",
                        df.to_csv(index=False).encode('utf-8'),
                        file_name=filename,
                        mime="text/csv"
                    )
            st.success(f"✅ {count} companies saved to {filename}")
        except Exception as e:
            st.error(f"❌ Error during scrape: {e}")

# --- EMAIL SCRAPE MODE ---
elif operation == "Email Scrape":
    st.header("Email Scrape from Website List")
    input_file = st.sidebar.text_input("CSV filename (with Website column):", "")
    if st.sidebar.button("Start Email Scraping"):
        if not input_file or not os.path.exists(input_file):
            st.sidebar.error("Invalid filename or file does not exist.")
        else:
            df = pd.read_csv(input_file)
            web_col = st.sidebar.text_input("Website column name:", "Website")
            out_name = f"emails_{os.path.splitext(os.path.basename(input_file))[0]}.csv"
            results = []
            with st.spinner("Scraping emails..."):
                for url in df[web_col].dropna():
                    clean = re.sub(r"\?.*", "", str(url)).rstrip('/')
                    try:
                        resp = requests.get(clean, timeout=5)
                        time.sleep(1)
                        emails = re.findall(r"[\w.%+-]+@[\w.-]+\.[A-Za-z]{2,}", resp.text)
                        email = emails[0] if emails else "Not Available"
                    except:
                        email = "Not Available"
                    results.append({"Website": clean, "Email": email})
            out_df = pd.DataFrame(results)
            out_df.to_csv(out_name, index=False)
            st.session_state.email_data = out_df
            st.session_state.email_filename = out_name
            with st.sidebar:
                st.markdown("### 📂 Email Results")
                st.write(f"`{out_name}`")
                st.dataframe(out_df)
                st.download_button(
                    "⬇️ Download Emails CSV",
                    out_df.to_csv(index=False).encode('utf-8'),
                    file_name=out_name,
                    mime="text/csv"
                )
            st.success(f"✅ Emails saved to {out_name}")

# --- MERGE DATA MODE ---
elif operation == "Merge Data":
    st.header("Merge LinkedIn & Email Data")
    link_file = st.text_input("LinkedIn CSV:", "linkedin_data.csv")
    email_file = st.text_input("Email CSV:", "emails.csv")
    if st.button("Merge Files"):
        if not os.path.exists(link_file):
            st.error(f"File not found: {link_file}")
        elif not os.path.exists(email_file):
            st.error(f"File not found: {email_file}")
        else:
            try:
                ldf = pd.read_csv(link_file)
                edf = pd.read_csv(email_file)
                if 'Email' not in edf.columns:
                    st.error("⚠️ 'Email' column missing in email file.")
                else:
                    ldf['Email'] = edf['Email']
                    merged = "merged_data_output.xlsx"
                    with pd.ExcelWriter(merged, engine='openpyxl') as writer:
                        ldf.to_excel(writer, index=False, sheet_name="MergedData")
                    buf = BytesIO()
                    with pd.ExcelWriter(buf, engine='openpyxl') as writer:
                        ldf.to_excel(writer, index=False, sheet_name="MergedData")
                    buf.seek(0)
                    st.session_state.merged_df = ldf
                    st.session_state.merged_file = merged
                    st.session_state.merged_bytes = buf.read()
                    st.success(f"✅ Merged saved as {merged}")
            except Exception as e:
                st.error(f"❌ Merge failed: {e}")
    if "merged_df" in st.session_state:
        with st.sidebar:
            st.markdown("### 📂 Merged Data Preview")
            st.write(f"`{st.session_state.merged_file}`")
            st.dataframe(st.session_state.merged_df)
            st.download_button(
                "⬇️ Download Excel",
                data=st.session_state.merged_bytes,
                file_name=st.session_state.merged_file,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

# --- EMAIL TEMPLATE VIEWER MODE ---
elif operation == "Email Template Viewer":
    st.header("Email Template Viewer")
    if st.sidebar.button("Load Template"):
        st.session_state.show_template = True
    if st.session_state.get("show_template", False):
        tpl = "email_template.html"
        if not os.path.exists(tpl):
            st.error(f"Template not found: {tpl}")
        else:
            with open(tpl, 'r', encoding='utf-8') as f:
                html = f.read()
            st.subheader("Rendered Template")
            st.components.v1.html(html, height=600, scrolling=True)
            with st.expander("Raw HTML"):
                st.code(html, language='html')

# --- SEND EMAIL MODE ---
elif operation == "Send Email":
    st.header("Send Emails from Merged Data")
    excel_file = st.sidebar.text_input("Excel filename:", "merged_data_output.xlsx")
    if st.sidebar.button("Start Sending Emails"):
        if not excel_file or not os.path.exists(excel_file):
            st.sidebar.error(f"File not found: {excel_file}")
        else:
            with st.spinner("Sending emails..."):
                result = subprocess.run(
                    ["python", "send_email.py", excel_file],
                    capture_output=True,
                    text=True
                )
            st.subheader("Successful Emails Sent")
            for ln in result.stdout.splitlines():
                if 'Email sent successfully to' in ln:
                    st.success(ln)
            success_count = sum(
                1 for ln in result.stdout.splitlines()
                if 'Email sent successfully to' in ln
            )
            st.info(f"Total emails sent successfully: {success_count}")

# --- LIVE TRACKING MODE ---
elif operation == "Live Tracking":
    st.header("📊 Live Email Tracking Data Viewer")
    track_file = st.sidebar.text_input("Enter tracking CSV filename:", "email_tracking_data.csv")
    refresh_sec = st.sidebar.number_input("Refresh interval (seconds):", min_value=1, value=5)

    try:
        from streamlit_autorefresh import st_autorefresh
    except ImportError:
        st.sidebar.error("Missing package: run 'pip install streamlit-autorefresh'")
        st.stop()

    st_autorefresh(interval=refresh_sec * 1000, limit=None, key="tracking_refresh")

    if os.path.exists(track_file):
        try:
            df_track = pd.read_csv(track_file)
            st.sidebar.markdown("### Live Tracking Data")
            st.sidebar.dataframe(df_track)
        except Exception as e:
            st.sidebar.error(f"Error reading tracking file: {e}")
    else:
        st.sidebar.error(f"File not found: {track_file}")

elif operation == "Evaluate Model":
    st.header("📊 Evaluate Email Interaction Prediction Model")

    if not os.path.exists("model_evaluation.py"):
        st.error("❌ model_evaluation.py file not found.")
    else:
        if st.button("Run Evaluation"):
            with st.spinner("Running evaluation script..."):
                result = subprocess.run(
                    ["python", "model_evaluation.py"],
                    capture_output=True,
                    text=True
                )
            st.subheader("📝 Evaluation Output")
            st.code(result.stdout, language="text")
            if result.stderr:
                st.error(result.stderr)


# --- ADVANCED LEAD SCORING MODE ---
elif operation == "Advanced Lead Scoring":
    st.header("📈 Advanced Lead Scoring Report Generator")

    hlcl_file = "HLCL.py"
    if not os.path.exists(hlcl_file):
        st.error("❌ HLCL.py not found.")
    else:
        if st.button("Run Scoring Script"):
            with st.spinner("Running HLCL.py..."):
                result = subprocess.run(["python", hlcl_file], capture_output=True, text=True)

            st.subheader("Script Output")
            st.code(result.stdout)
            if result.stderr:
                st.error(result.stderr)

            report_file = "Advanced_Lead_Scoring_Report.csv"
            if os.path.exists(report_file):
                df = pd.read_csv(report_file)
                st.sidebar.markdown("### 📊 Lead Scoring Report")
                st.sidebar.dataframe(df)
                st.download_button(
                    "⬇️ Download Report CSV",
                    df.to_csv(index=False).encode('utf-8'),
                    file_name=report_file,
                    mime="text/csv"
                )
            else:
                st.error("Report file not found after running HLCL.py.")
# --- CAMPAIGN REPORT SUMMARY MODE ---
elif operation == "Campaign Report Summary":
    st.header("📋 Campaign Analytics Summary Report")

    report_file = "report.py"
    if not os.path.exists(report_file):
        st.error("❌ report.py not found.")
    else:
        if st.button("Run Report Script"):
            with st.spinner("Running report.py..."):
                result = subprocess.run(["python", report_file], capture_output=True, text=True)

            st.subheader("📝 Script Output")
            st.code(result.stdout)
            if result.stderr:
                st.error(result.stderr)

            summary_file = "Campaign_Analytics_Summary.csv"
            if os.path.exists(summary_file):
                df_summary = pd.read_csv(summary_file)
                st.sidebar.markdown("### 📈 Analytics Summary")
                st.sidebar.dataframe(df_summary)
                st.download_button(
                    "⬇️ Download Summary CSV",
                    df_summary.to_csv(index=False).encode('utf-8'),
                    file_name=summary_file,
                    mime="text/csv"
                )
            else:
                st.error("Summary file not found after running report.py.")




elif operation == "Create Jira Tasks":
    st.header("Run Jira Automation Script")

    if st.button("Run Script"):
        with st.spinner("Running ji.py..."):
            result = subprocess.run(
                ["python", "ji.py"],
                capture_output=True,
                text=True
            )

        st.subheader("Output")
        st.code(result.stdout)

        if result.stderr:
            st.subheader("Errors")
            st.error(result.stderr)


elif operation == "Create GitHub Repo from Tasks":
    st.header("Create GitHub Repo and Push Jira Tasks")

    if st.button("Run giit.py Script"):
        with st.spinner("Running giit.py..."):
            result = subprocess.run(
                ["python", "giit.py"],
                capture_output=True,
                text=True
            )

        # st.subheader("Output")
        # st.code(result.stdout)

        st.subheader("📤 Git Output")
        if result.stdout.strip():
            st.code(result.stdout, language="text")
        else:
            st.info("✅ No standard output.")
        stderr_clean = result.stderr.strip()
        if stderr_clean and "error" in stderr_clean.lower():
            st.subheader("⚠️ Git Errors")
            st.error(stderr_clean)


elif operation == "Generate Test Cases":
    st.header("🧪 Generate Test Cases from Jira Tasks")

    if st.button("Run test.py Script"):
        with st.spinner("Running test.py..."):
            result = subprocess.run(
                ["python", "test.py"],
                capture_output=True,
                text=True
            )

        st.subheader("📤 Test Case Output")
        if result.stdout.strip():
            st.code(result.stdout, language="text")
        else:
            st.info("✅ No standard output.")

        stderr_clean = result.stderr.strip()
        if stderr_clean and "error" in stderr_clean.lower():
            st.subheader("⚠️ Errors")
            st.error(stderr_clean)
