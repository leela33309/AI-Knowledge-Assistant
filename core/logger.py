import csv
import os
from datetime import datetime

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

LOG_FILE = os.path.join(
    BASE_DIR,
    "logs.csv"
)


# =========================
# CREATE LOG FILE
# =========================
def create_log_file():

    if not os.path.isfile(LOG_FILE):

        with open(
            LOG_FILE,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "timestamp",
                "query",
                "answer",
                "latency",
                "sources_used",
                "response_type",
                "status"
            ])


# =========================
# DETECT RESPONSE TYPE
# =========================
def detect_response_type(answer):

    text = answer.lower()

    if "⚡ cached response" in text:
        return "CACHE"

    elif "🧠 knowledge graph response" in text:
        return "GRAPH"

    elif "⚠️ error" in text:
        return "ERROR"

    else:
        return "LLM"


# =========================
# DETECT STATUS
# =========================
def detect_status(answer):

    if "⚠️ error" in answer.lower():
        return "FAILED"

    return "SUCCESS"


# =========================
# MAIN LOGGER
# =========================
def log_query(
    query,
    answer,
    latency,
    sources_used
):

    create_log_file()

    response_type = detect_response_type(
        answer
    )

    status = detect_status(
        answer
    )

    with open(
        LOG_FILE,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            query,
            answer,
            latency,
            sources_used,
            response_type,
            status
        ])