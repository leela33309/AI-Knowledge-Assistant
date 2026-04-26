import os
import json
from datetime import datetime

DATA_FOLDER = "../data"
os.makedirs(DATA_FOLDER, exist_ok=True)

documents = [
    {
        "title": "Leave Policy",
        "type": "policy",
        "content": "Employees are entitled to 20 paid leaves per year. Leaves must be approved by the manager.",
        "tags": ["HR", "leave"],
    },
    {
        "title": "Password Reset Guide",
        "type": "guide",
        "content": "To reset your password, go to settings, click on security, and select reset password.",
        "tags": ["IT", "security"],
    },
    {
        "title": "Work From Home Policy",
        "type": "policy",
        "content": "Employees can work from home up to 2 days per week with prior approval.",
        "tags": ["HR", "WFH"],
    }
]

for i, doc in enumerate(documents):
    doc["date"] = str(datetime.now())

    file_path = os.path.join(DATA_FOLDER, f"doc_{i}.json")

    with open(file_path, "w") as f:
        json.dump(doc, f, indent=4)

print("✅ Data generated successfully!")
