import json
import time
import requests

API_URL = "http://127.0.0.1:8000/ask"

# =========================
# LOAD QUESTIONS
# =========================
with open(
    "evaluation/questions.json",
    "r"
) as f:

    questions = json.load(f)

# =========================
# METRICS
# =========================
total_questions = len(questions)

correct_retrievals = 0

total_latency = 0

# =========================
# EVALUATION LOOP
# =========================
for item in questions:

    question = item["question"]

    expected_source = item[
        "expected_source"
    ]

    start = time.time()

    response = requests.post(
        API_URL,
        json={
            "question": question
        }
    )

    latency = time.time() - start

    total_latency += latency

    data = response.json()

    sources = data.get(
        "sources",
        []
    )

    retrieved_sources = []

    for s in sources:

        if isinstance(s, dict):

            retrieved_sources.append(
                s.get("source", "")
            )

    # =====================
    # RECALL@K
    # =====================
    if expected_source in retrieved_sources:

        correct_retrievals += 1

    # =====================
    # DISPLAY
    # =====================
    print("\n=====================")

    print(f"Question: {question}")

    print(f"Expected: {expected_source}")

    print(
        f"Retrieved: {retrieved_sources}"
    )

    print(
        f"Latency: {round(latency, 2)} sec"
    )

# =========================
# FINAL METRICS
# =========================
recall_at_k = (
    correct_retrievals / total_questions
) * 100

avg_latency = (
    total_latency / total_questions
)

print("\n=====================")
print("FINAL EVALUATION")
print("=====================")

print(
    f"Recall@K: {round(recall_at_k, 2)}%"
)

print(
    f"Average Latency: {round(avg_latency, 2)} sec"
)