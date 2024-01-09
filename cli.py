import argparse
import api

def main():
    parser = argparse.ArgumentParser(description='CLI Example')
    parser.add_argument('--project', type=str, help='Specify project key')
    parser.add_argument('--days', type=int, help='Specify days prior to query')
    args = parser.parse_args()
    project = "IT" if not args.project else args.project
    days = 90 if not args.days else args.days
    api.generate_report(project, days)

if __name__ == "__main__":
    main()