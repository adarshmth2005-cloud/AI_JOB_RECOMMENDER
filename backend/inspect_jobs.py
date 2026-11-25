
import csv

file_path = r"C:\Users\Adarsh\AI_JOB_RECOMMENDER\archive (1)\job_descriptions.csv"

with open(file_path, "r", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)

    print("===== JOB DATASET COLUMNS =====")
    print(reader.fieldnames)

    print("\n===== FIRST 2 JOB RECORDS =====")

    for i, row in enumerate(reader):
        if i == 2:
            break

        for key, value in row.items():
            print(f"{key}: {str(value)[:200]}")

        print("-------------------------")
