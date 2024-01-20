from lib import jira, llm, csv

def generate_report(project: str, days: int, jql: str):
    jql = jql if jql != "" else f"project = {project} AND createdDate >= {jira.format_date(days)} ORDER BY createdDate DESC"
    print(f"Query: {jql}")
    jira_issues = []
    jira.fetch_issues(jira_issues, jql)

    print(f"{len(jira_issues)} total issues fetched...")
    issues = jira.parse_issues(jira_issues)

    samples = [i["conversation"] for i in issues[:25]]
    samples = "Issue: \n".join(samples)

    print("Creating categories...")
    categories = llm.generate_categories(samples)

    print("Classifying issues...")
    rows = llm.generate_classifications(issues, categories)

    print("Writing to csv...")
    csv.generate_issues_report(rows)

    csv.generate_stats_report()