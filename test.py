import os
import re
from ji import extract_tasks  

# ----------- Utility: Sanitize Branch Name and Filename -------------
def sanitize_branch_name(title):
    """Sanitize branch name for Git and filename purposes."""
    branch = title.strip().lower().replace(" ", "-")
    branch = re.sub(r'[^a-z0-9\-_.]', '', branch)
    branch = re.sub(r'-{2,}', '-', branch).strip('-')
    return branch

# ----------- Generate Test Case for Each Task -------------
def generate_test_case(task):
    """Generate a test case based on the extracted task details."""
    
    # Debugging: Print the task dictionary to inspect its structure
    print("Task:", task)  # This will print the structure of the task dictionary

    # Safely handle missing keys using 'get' to avoid KeyError
    test_case_id = f"TC-{task.get('ticket_id', 'unknown')}"  # Use 'get' to avoid KeyError
    test_case_title = task.get('title', 'No Title Provided')
    test_case_description = task.get('description', 'No Description Provided')

    # Creating test case template
    test_case = f"""
    ## Test Case ID: {test_case_id}
    - **Title**: {test_case_title}
    - **Preconditions**: Ensure user is logged in (example)
    - **Test Steps**:
      1. Navigate to the task page
      2. Verify the task title
      3. Check the task description
    - **Expected Result**: Task details should be displayed correctly.
    - **Link to Jira Ticket**: [Jira Ticket](https://jira.company.com/browse/{task.get('ticket_id', 'unknown')})
    """

    # Saving the test case to a markdown file
    filename = f"tc-{sanitize_branch_name(test_case_title)}.md"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(test_case)

    print(f"Test case created: {filename}")

# ----------- Step 1: Extract Tasks from Word Doc or Jira (if connected) -------------
def extract_jira_tasks(docx_path):
    """Assuming this function extracts tasks from a Word document."""
    tasks = extract_tasks(docx_path)  
    return tasks

# ----------- Step 2: Run Test Case Creation Process -------------
if __name__ == "__main__":
    # Path to your Word document or Jira tickets info
    docx_path = "Sales Process Automation (1).docx"  
    
    # Extract tasks from the document
    tasks = extract_jira_tasks(docx_path)

    # Generate and save test cases for each task
    for task in tasks:
        generate_test_case(task)
