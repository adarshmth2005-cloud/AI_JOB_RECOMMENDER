
import requests

API_URL = "http://127.0.0.1:5000/api/resumes/"

response = requests.get(API_URL)

if response.status_code == 200:
    data = response.json()

    print("\n===== RESUME DATABASE =====")
    print("Total Resumes:", data["total_resumes"])
    print("Total Pages:", data["total_pages"])

    print("\n===== RESUME RECORDS =====")

    for resume in data["resumes"]:
        print("--------------------------")
        print("ID:", resume["id"])
        print("Dataset ID:", resume["dataset_id"])
        print("Category:", resume["category"])
        print("Skills:", resume["skills"])

else:
    print("API Error:", response.status_code)
