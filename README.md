# JCAT Py
A Python script to query Jira issues, create categories, and classify each issue into a category, then generate CSVs from the data.

## Secrets
Export the following values in your terminal session before running jcat.py
```sh
export JIRA_API_KEY=<Your Jira API Key> \
export OPENAI_API_KEY=<Your OpenAI API Key>
```

## Usage
- Queries the IT Jira project for issues in the last 90 days and categorizes issues.
```sh
python cli.py --project IT
```
- Queries the IT Jira project key for issues in the last 10 days and categorizes issues.
```sh
python cli.py --project IT --days 10
```
- Queries with custom JQL and categorizes issues.
```sh
python cli.py --jql "project = IT AND assignee = 'eric.rodriguez@gusto.com'"
```