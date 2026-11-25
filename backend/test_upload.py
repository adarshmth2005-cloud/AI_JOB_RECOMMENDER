
import requests

url = "http://127.0.0.1:5000/api/resumes/upload"

file_path = r"C:\Users\Adarsh\1_ADARSH_KUMAR_DOCUMENTS\CV of Adarsh kumar\AdarshKumarResume (1).pdf"

with open(file_path, "rb") as resume_file:
    files = {
        "resume": (
            "sample_resume.pdf",
            resume_file,
            "application/pdf"
        )
    }

    response = requests.post(url, files=files)

print("Status Code:", response.status_code)
print("Response:")
print(response.json())
