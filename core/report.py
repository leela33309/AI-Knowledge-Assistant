import pandas as pd
import matplotlib.pyplot as plt
import os

LOG_FILE = "logs.csv"

# =========================
# CHECK FILE EXISTS
# =========================
if not os.path.exists(LOG_FILE):
    print("No logs.csv found yet.")
    exit()

# =========================
# LOAD DATA
# =========================
df = pd.read_csv(LOG_FILE)

# =========================
# CLEAN DATA
# =========================
df["latency"] = pd.to_numeric(
    df["latency"],
    errors="coerce"
)

df["sources_used"] = pd.to_numeric(
    df["sources_used"],
    errors="coerce"
)

df["timestamp"] = pd.to_datetime(
    df["timestamp"],
    errors="coerce"
)

# =========================
# SUMMARY
# =========================
print("\n📊 AI KNOWLEDGE ASSISTANT FINAL REPORT")
print("-" * 50)

print("Total Queries        :", len(df))
print("Average Latency      :", round(df["latency"].mean(), 2), "sec")
print("Fastest Query        :", round(df["latency"].min(), 2), "sec")
print("Slowest Query        :", round(df["latency"].max(), 2), "sec")
print("Average Sources Used :", round(df["sources_used"].mean(), 2))

# =========================
# RESPONSE TYPE COUNTS
# =========================
if "response_type" in df.columns:

    print("\n🧠 Response Breakdown")

    print(
        df["response_type"]
        .value_counts()
        .to_string()
    )

# =========================
# STATUS COUNTS
# =========================
if "status" in df.columns:

    print("\n📌 Status Breakdown")

    print(
        df["status"]
        .value_counts()
        .to_string()
    )

# =========================
# TOP SLOW QUERIES
# =========================
print("\n🐢 Top 5 Slowest Queries")

slow = df.sort_values(
    "latency",
    ascending=False
).head(5)

for _, row in slow.iterrows():

    print(
        f"- {row['query']} "
        f"({row['latency']} sec)"
    )

# =========================
# CHART 1 LATENCY
# =========================
plt.figure(figsize=(10, 5))

plt.plot(
    df["latency"],
    marker="o"
)

plt.title("Query Response Time")
plt.xlabel("Query Number")
plt.ylabel("Latency (sec)")
plt.grid(True)
plt.tight_layout()
plt.show()

# =========================
# CHART 2 RESPONSE TYPES
# =========================
if "response_type" in df.columns:

    plt.figure(figsize=(8, 5))

    df["response_type"] \
        .value_counts() \
        .plot(kind="bar")

    plt.title("Response Type Usage")
    plt.xlabel("Type")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.show()

# =========================
# CHART 3 DAILY USAGE
# =========================
if "timestamp" in df.columns:

    daily = df.groupby(
        df["timestamp"].dt.date
    ).size()

    plt.figure(figsize=(10, 5))

    daily.plot(
        kind="bar"
    )

    plt.title("Daily Query Usage")
    plt.xlabel("Date")
    plt.ylabel("Queries")
    plt.tight_layout()
    plt.show()