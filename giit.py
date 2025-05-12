import requests
import os
import subprocess
import re
from ji import extract_tasks  

# ----------- GitHub Configuration -------------
GITHUB_USERNAME = ""  
GITHUB_TOKEN = "" 
REPO_NAME = "auto-created-repo"
GITHUB_API_URL = "https://api.github.com"

# ----------- Utility: Sanitize Branch Name and Filename -------------
def sanitize_branch_name(title):
    # Lowercase, replace spaces with dashes
    branch = title.strip().lower().replace(" ", "-")
    # Remove special characters not allowed in Git refs
    branch = re.sub(r'[^a-z0-9\-_.]', '', branch)
    branch = re.sub(r'-{2,}', '-', branch).strip('-')
    return branch

# ----------- Step 1: Create GitHub Repo -------------
def create_github_repo():
    url = f"{GITHUB_API_URL}/user/repos"
    data = {
        "name": REPO_NAME,
        "private": False,
        "auto_init": True,
        "description": "Repo auto-created from Jira tasks"
    }

    response = requests.post(url, json=data, auth=(GITHUB_USERNAME, GITHUB_TOKEN))

    if response.status_code == 201:
        # print(f"GitHub repo '{REPO_NAME}' created.")
        return f"https://github.com/{GITHUB_USERNAME}/{REPO_NAME}.git"
    else:
        print("Failed to create GitHub repo:")
        print(response.text)
        return None

# ----------- Step 2: Clone the Repo Locally -------------
def clone_repo(repo_url):
    subprocess.run(["git", "clone", repo_url])
    os.chdir(REPO_NAME)

# ----------- Step 3: Create Branches and Commit Files -------------
def create_branches_and_commit(tasks):
    for task in tasks:
        branch_name = sanitize_branch_name(task["title"])
        subprocess.run(["git", "checkout", "-b", branch_name])

        # Create safe filename
        filename = f"{branch_name}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# {task['title']}\n\n{task['description']}")

        subprocess.run(["git", "add", filename])
        subprocess.run(["git", "commit", "-m", f"Add task: {task['title']}"])
        subprocess.run(["git", "push", "--set-upstream", "origin", branch_name])

# ----------- Step 4: Run Everything -------------
if __name__ == "__main__":
    docx_path = "Sales Process Automation (1).docx"
    tasks = extract_tasks(docx_path)

    repo_url = create_github_repo()
    if repo_url:
        clone_repo(repo_url)
        create_branches_and_commit(tasks)
