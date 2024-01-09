from lib import jira, llm
import json
import csv
from tqdm import tqdm

project = "BT"
days = 90

print(f"Fetching {project} issues in the last {days} days...")
jira_issues = jira.get_issues(project, days)
issues = jira.parse_issues(jira_issues)

samples = [i["conversation"] for i in issues[:100]]
samples = "Issue: \n".join(samples)
print("Creating categories...")
categories = llm.get_categories(samples)

print("Classifying issues...")
rows = []
for issue in tqdm(issues):
    res = llm.classify(issue["conversation"], categories)
    data = json.loads(res)
    key = issue["key"]
    category = data["category"]
    subcategory = data["subcategory"]
    rows.append([key, issue["summary"], category, subcategory])

print("Writing to csv...")
with open("output.csv", mode="w", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["key", "summary", "category", "subcategory"])
    for row in tqdm(rows):
        writer.writerow([row[0], row[1], row[2], row[3]])

breakdown = {}
for row in rows:
    #BAD!
    if row[2] in breakdown:
        if row[3] in breakdown[row[2]]:
            breakdown[row[2]][row[3]] += 1
        else:
            breakdown[row[2]][row[3]] = 1
    else:
        breakdown[row[2]] = {}
        breakdown[row[2]][row[3]] = 1
with open("stats.csv", mode="w", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["category", "subcategory", "count"])
    for k, v in breakdown.items():
        for key, value in v.items():
            writer.writerow([k, key, value])