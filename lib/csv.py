import csv
from tqdm import tqdm

def generate_issues_report(rows: list[str]):
    with open("issues.csv", mode="w", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["key", "summary", "category", "subcategory"])
        for row in tqdm(rows):
            writer.writerow([row[0], row[1], row[2], row[3]])

def generate_stats_report():
    with open("issues.csv", mode="r", newline="", encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file)
        breakdown = {}
        for row in csv_reader:
            try:
                if row[2] in breakdown:
                    if row[3] in breakdown[row[2]]:
                        breakdown[row[2]][row[3]] += 1
                    else:
                        breakdown[row[2]][row[3]] = 1
                else:
                    breakdown[row[2]] = {}
                    breakdown[row[2]][row[3]] = 1
            except Exception as e:
                print(e)
                continue
    with open("stats.csv", mode="w", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["category", "subcategory", "count"])
        for k, v in breakdown.items():
            for key, value in v.items():
                writer.writerow([k, key, value])