import os
import json
from datetime import datetime

# =========================
# OUTPUT DIRECTORY
# =========================
OUTPUT_DIR = "data/generated_docs"

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

# =========================
# SYNTHETIC DOCUMENTS
# =========================
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
        "tags": ["onboarding", "new_joiner"],
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
        "tags": ["faq", "support"],
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

# =========================
# GENERATE FILES
# =========================
for index, doc in enumerate(
    documents,
    start=1
):

    base_filename = f"doc_{index}"

    text_path = os.path.join(
        OUTPUT_DIR,
        f"{base_filename}.txt"
    )

    metadata_path = os.path.join(
        OUTPUT_DIR,
        f"{base_filename}.json"
    )

    # =====================
    # SAVE TEXT CONTENT
    # =====================
    with open(
        text_path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            doc["content"].strip()
        )

    # =====================
    # METADATA
    # =====================
    metadata = {
        "title": doc["title"],
        "type": doc["type"],
        "tags": doc["tags"],
        "source": text_path,
        "created_date": str(
            datetime.now().date()
        )
    }

    # =====================
    # SAVE METADATA
    # =====================
    with open(
        metadata_path,
        "w",
        encoding="utf-8"
    ) as meta_file:

        json.dump(
            metadata,
            meta_file,
            indent=4
        )

# =========================
# SUCCESS MESSAGE
# =========================
print(
    f"✅ Generated {len(documents)} synthetic documents"
)

print(
    f"📁 Output Location: {OUTPUT_DIR}"
)