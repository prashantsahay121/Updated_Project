
# 📂 Jira to GitHub Task Automation & Test Case Generator

This project automates the end-to-end process of reading tasks from a `.docx` document, creating Jira tickets for each task, creating GitHub branches, pushing task files, and generating markdown test cases. It is ideal for QA teams, developers, or managers to streamline task tracking and documentation using Python.

---

## 🚀 Key Features

- 📄 **Task Extraction**: Extracts structured task titles and descriptions from a Word `.docx` file.
- 🐞 **Jira Ticket Creation**: Automatically creates tasks in Jira using REST API.
- 🌿 **GitHub Branch Automation**: Creates a GitHub repo and branches for each task, and commits `.md` files.
- 🧪 **Test Case Generation**: Generates test cases in Markdown format from the same task input.

---

## 🗂 Project Structure

| File Name     | Purpose                                                                 |
|---------------|-------------------------------------------------------------------------|
| `ji.py`       | Extracts tasks from `.docx` and creates Jira tasks using REST API       |
| `giit.py`     | Creates GitHub repo, branches, and pushes task files (`.md`)            |
| `test.py`     | Generates structured test cases in Markdown format for each task        |


---

## 🧾 Use Case

Suppose you have a document titled `Sales Process Automation (1).docx` with multiple tasks written as:

```
Task 1: Set up login page
This task includes designing the login page and backend validation.

Task 2: Integrate API
Connect the frontend to the user authentication API and validate session.
```

This system will:

1. Create Jira tickets like `SAL-101`, `SAL-102` for each task.
2. Create a GitHub repo (e.g., `auto-created-repo`), with branches like `set-up-login-page`, `integrate-api`.
3. Push each task as a `.md` file in its branch.
4. Generate test case files like `tc-set-up-login-page.md`.

---

## ⚙️ Setup Instructions

### 1. Install Dependencies

```bash
pip install python-docx requests
```

---

## 🔑 Configuration

Update the following values inside the scripts before running:

### 🔹 In `ji.py` (Jira Credentials):

```python
JIRA_URL = "https://your-domain.atlassian.net"
EMAIL = "your-email@example.com"
API_TOKEN = "your-jira-api-token"
PROJECT_KEY = "SAL"  # Replace with your project key
```

### 🔹 In `giit.py` (GitHub Credentials):

```python
GITHUB_USERNAME = "your-github-username"
GITHUB_TOKEN = "your-github-token"
REPO_NAME = "auto-created-repo"
```

---

## 🧪 Execution Steps

### 🔹 Step 1: Create Jira Tickets

```bash
python ji.py
```

- Parses `.docx` file and creates tickets in Jira for each task.

---

### 🔹 Step 2: Create GitHub Repo, Branches, and Commit Files

```bash
python giit.py
```

- Creates a public repo, creates branches based on task titles, and pushes `.md` files for each task.

---

### 🔹 Step 3: Generate Test Case Files

```bash
python test.py
```

- Creates structured test case markdown files with steps, expected results, and placeholder for Jira ticket links.

---

## 📄 Sample Output Files

- `auto-created-repo/`: GitHub repository with branches per task.
- `set-up-login-page.md`: Markdown file pushed to GitHub per task.
- `tc-set-up-login-page.md`: Generated test case file in Markdown.
- Jira Issues: Created in your Jira project with correct titles and descriptions.

---

## 📘 Example Test Case Output

```markdown
## Test Case ID: TC-SAL-101
- **Title**: Set up login page
- **Preconditions**: Ensure user is logged in
- **Test Steps**:
  1. Navigate to the login page
  2. Verify the UI loads properly
  3. Validate backend functionality
- **Expected Result**: Login should succeed with valid credentials.
- **Link to Jira Ticket**: [Jira Ticket](https://jira.company.com/browse/SAL-101)
```

---

## 🛡️ Security Notes

- Do **not** hardcode API tokens in production projects.
- Use environment variables or `.env` files to securely manage credentials.

---

## 🧑‍💻 Author

**Prashant Kumar**  
Email: `prashantsahay121@gmail.com`  
Project Type: Internal Tool / Automation Script

---

## 📌 License

This project is open for educational and personal use. Feel free to extend it with more integrations like Confluence, Slack alerts, or test execution hooks.
