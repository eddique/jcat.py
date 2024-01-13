import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta
from tqdm import tqdm

load_dotenv()

def fetch_issues(issues: list[dict], jql: str = "", start_at: int = 0, count: int = 0):
    url = "https://jira.gustocorp.com/rest/api/2/search"
    headers = {
        "Authorization": "Bearer " + os.getenv("JIRA_API_KEY") ,
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    data = {
        "expand": [
            "comment"
        ],
        "fields": [
            "summary",
            "description",
            "comment"
        ],
        "jql": jql,
        "maxResults": 10000,
        "startAt": start_at
    }
    print(f"Fetching issues page {count+1}...")
    try:
        r = requests.post(url, headers=headers, json=data)
        payload = r.json()
        start = payload["startAt"]
        total = payload["total"]
        max = payload["maxResults"]
        issues.extend(payload["issues"])
        if start + max < total:
            fetch_issues(issues, jql, (start + max), count+1)

    except Exception as e:
        print(e)    

def parse_issues(issues):
    prompt = []
    for i in tqdm(issues):
        key = i["key"]
        fields = i["fields"]
        summary = fields["summary"]
        description = "" if not fields["description"] else fields["description"]
        comments = fields["comment"]["comments"]
        issue = {
            "id": i["id"],
            "key": key,
            "conversation": "",
            "summary": summary
        }
        issue["conversation"] += "Summary: " + summary + "\n"
        issue["conversation"] += "Description: " + description + "\n"
        for comment in comments:
            issue["conversation"] += "User: " + comment["body"] + "\n"
        prompt.append(issue)
    return prompt

def format_date(subtract_days):
    today = datetime.today()

    new_date = today - timedelta(days=subtract_days)

    formatted_date = new_date.strftime('%Y-%m-%d')
    
    return formatted_date