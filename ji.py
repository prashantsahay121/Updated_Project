from docx import Document
import requests
from requests.auth import HTTPBasicAuth
import json

# ----------- Step 1: Configuration -------------
JIRA_URL = ""  
API_TOKEN = ""               # 🔁 Replace with your API token
EMAIL = "prashantsahay121@gmail.com"               
PROJECT_KEY = "SAL"                            

# Jira auth and headers
auth = HTTPBasicAuth(EMAIL, API_TOKEN)
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# ----------- Step 2: Extract Tasks from .docx -------------
def extract_tasks(doc_path):
    doc = Document(doc_path)
    tasks = []
    current_task = None

    for para in doc.paragraphs:
        text = para.text.strip()
        if text.startswith("Task"):
            if current_task:
                tasks.append(current_task)
            current_task = {"title": text, "description": ""}
        elif current_task:
            current_task["description"] += text + "\n"
    
    if current_task:
        tasks.append(current_task)
    
    return tasks

# ----------- Step 3: Create Jira Tickets -------------
def create_jira_ticket(task):
    adf_description = {
        "type": "doc",
        "version": 1,
        "content": [
            {
                "type": "paragraph",
                "content": [
                    {
                        "text": task["description"],
                        "type": "text"
                    }
                ]
            }
        ]
    }

    data = {
        "fields": {
            "project": {"key": PROJECT_KEY},
            "summary": task["title"],
            "description": adf_description,
            "issuetype": {"name": "Task"}
        }
    }

    response = requests.post(
        f"{JIRA_URL}/rest/api/3/issue",
        headers=headers,
        auth=auth,
        data=json.dumps(data)
    )

    if response.status_code == 201:
        ticket_key = response.json().get("key")
        print(f"Ticket Created: {ticket_key} - {task['title']}")
    else:
        print(f"Failed to create ticket: {task['title']}")
        print(response.text)

# ----------- Step 4: Run All Together -------------
if __name__ == "__main__":
    docx_path = "Sales Process Automation (1).docx" 
    tasks = extract_tasks(docx_path)
    print(f"Total Tasks Found: {len(tasks)}\n")

    for i, task in enumerate(tasks, 1):
        print(f"Creating Task {i}...")
        create_jira_ticket(task)
