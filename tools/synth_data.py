import os
import json
from datetime import datetime

# Output folder
OUTPUT_DIR = "data/generated_docs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


documents = [
    {
        "title": "HR Leave Policy",
        "type": "policy",
        "tags": ["hr", "leave"],
        "content": """
Employees are entitled to 20 paid leaves annually.
Sick leave requires manager approval after 2 consecutive days.
Unused leave can be carried forward up to 10 days.
"""
    },

    {
        "title": "Work From Home Policy",
        "type": "policy",
        "tags": ["remote", "wfh"],
        "content": """
Employees may work from home twice per week with manager approval.
WFH requests should be raised one day in advance.
Availability during business hours is mandatory.
"""
    },

    {
        "title": "New Employee Onboarding Guide",
        "type": "guide",
        "tags": ["onboarding", "new joiner"],
        "content": """
Day 1 includes laptop allocation, email setup, HR induction and project introduction.
Complete mandatory training modules within first 7 days.
"""
    },

    {
        "title": "VPN Access SOP",
        "type": "sop",
        "tags": ["it", "vpn"],
        "content": """
Install VPN client from company portal.
Login using employee ID and MFA authentication.
Report connection issues to IT helpdesk.
"""
    },

    {
        "title": "Password Security Guidelines",
        "type": "security",
        "tags": ["security", "password"],
        "content": """
Passwords must contain minimum 12 characters.
Use uppercase, lowercase, numbers and symbols.
Passwords expire every 90 days.
"""
    },

    {
        "title": "Frequently Asked Questions",
        "type": "faq",
        "tags": ["faq"],
        "content": """
Q: How to apply leave?
A: Use HRMS portal.

Q: How to raise IT ticket?
A: Use internal helpdesk portal.

Q: How to reset password?
A: Contact IT support.
"""
    }
]


for i, doc in enumerate(documents, start=1):
    filename = f"{OUTPUT_DIR}/doc_{i}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(doc["content"].strip())

    metadata = {
        "title": doc["title"],
        "type": doc["type"],
        "tags": doc["tags"],
        "date": str(datetime.now().date())
    }

    meta_file = f"{OUTPUT_DIR}/doc_{i}.json"

    with open(meta_file, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)

print("✅ Synthetic documents generated successfully!")
print("📁 Location:", OUTPUT_DIR)