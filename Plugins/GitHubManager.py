import os
from github import Github
from dotenv import dotenv_values

env_vars = dotenv_values(".env")
GITHUB_TOKEN = env_vars.get("GITHUB_TOKEN")

if GITHUB_TOKEN:
    g = Github(GITHUB_TOKEN)
else:
    print("Warning: GITHUB_TOKEN not found. GitHubManager will be limited.")

def can_handle(command):
    return any(keyword in command.lower() for keyword in ["github", "repository", "repo issues", "pr status", "create issue"])

def execute(command):
    if not GITHUB_TOKEN:
        return "I cannot access GitHub without a GITHUB_TOKEN configured in your .env file."

    try:
        if "list issues for" in command.lower():
            repo_name = command.lower().split("list issues for")[1].strip()
            repo = g.get_user().get_repo(repo_name)
            issues = repo.get_issues(state="open")
            response = f"Open issues for {repo_name}:\n"
            for issue in issues:
                response += f"- #{issue.number}: {issue.title} (by {issue.user.login})\n"
            return response
        elif "create issue in" in command.lower() and "title" in command.lower():
            parts = command.lower().split("create issue in")[1].split("title")
            repo_name = parts[0].strip()
            issue_title = parts[1].strip()
            repo = g.get_user().get_repo(repo_name)
            issue = repo.create_issue(title=issue_title)
            return f"Created issue #{issue.number}: {issue.title} in {repo_name}."
        elif "pr status for" in command.lower():
            repo_name = command.lower().split("pr status for")[1].strip()
            repo = g.get_user().get_repo(repo_name)
            pulls = repo.get_pulls(state="open")
            response = f"Open Pull Requests for {repo_name}:\n"
            for pull in pulls:
                response += f"- #{pull.number}: {pull.title} (by {pull.user.login}) - {pull.html_url}\n"
            return response
        else:
            return "GitHub command not understood. Try 'list issues for [repo_name]' or 'create issue in [repo_name] title [issue_title]'."
    except Exception as e:
        return f"Error interacting with GitHub: {e}. Make sure the repository exists and your token has the necessary permissions."

