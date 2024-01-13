from lib import jira, llm, csv
import json
from tqdm import tqdm

def generate_report(project: str, days: int, jql: str):
    print(f"Fetching {project} issues in the last {days} days...")
    jql = jql if jql != "" else f"project = {project} AND createdDate >= {jira.format_date(days)} ORDER BY createdDate DESC"
    print(f"Query: {jql}")
    jira_issues = []
    jira.fetch_issues(jira_issues, jql)
    print(f"Issues {len(jira_issues)}")
    issues = jira.parse_issues(jira_issues)

    samples = [i["conversation"] for i in issues[:50]]
    samples = "Issue: \n".join(samples)

    print("Creating categories...")
    categories = llm.get_categories(samples)

    print("Classifying issues...")
    rows = []
    for issue in tqdm(issues[:100]):
        try:
            res = llm.classify(issue["conversation"], categories)
            data = json.loads(res)
            key = issue["key"]
            category = data["category"]
            subcategory = data["subcategory"]
            rows.append([key, issue["summary"], category, subcategory])
        except Exception as e:
            print(e)
            continue

    print("Writing to csv...")
    csv.generate_issues_report(rows)

    csv.generate_stats_report()