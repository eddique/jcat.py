import argparse
import api

def main():
    parser = argparse.ArgumentParser(description='A CLI to generate reports on Jira issues based on category')
    parser.add_argument('--project', type=str, help='Specify project key')
    parser.add_argument('--days', type=int, help='Specify days prior to query')
    parser.add_argument('--jql', type=str, help='Use a custom JQL query')
    args = parser.parse_args()
    project = args.project if args.project else "IT"
    days = args.days if args.days else 90
    jql = args.jql if args.jql else ""
    api.generate_report(project, days, jql)

if __name__ == "__main__":
    main()