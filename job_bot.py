import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9"
}

# 🔹 Fetch jobs from Indeed (basic + safe)
def fetch_indeed_jobs():
    jobs = []
    url = "https://in.indeed.com/jobs?q=QA+Automation&l=India&fromage=3"

    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        for card in soup.find_all("a"):
            title = card.get_text(strip=True)

            if title and len(title) > 10 and "QA" in title.upper():
                jobs.append({
                    "Title": title,
                    "Company": "Unknown",
                    "Source": "Indeed"
                })

    except Exception as e:
        print("❌ Error fetching Indeed jobs:", e)

    return jobs


# 🔹 Fallback jobs (prevents failure)
def fallback_jobs():
    return [
        {"Title": "QA Automation Lead Selenium", "Company": "Fallback", "Source": "Static"},
        {"Title": "Senior SDET API Automation", "Company": "Fallback", "Source": "Static"},
        {"Title": "Test Automation Architect Java Selenium", "Company": "Fallback", "Source": "Static"}
    ]


# 🔹 Scoring logic
def score_job(title):
    score = 0
    title_lower = title.lower()

    if "playwright" in title_lower or "selenium" in title_lower:
        score += 3
    if "api" in title_lower:
        score += 2
    if "lead" in title_lower or "architect" in title_lower or "manager" in title_lower:
        score += 2
    if "automation" in title_lower:
        score += 1

    return score


# 🔹 Main execution
def main():
    print("🚀 Starting Job Bot...")

    jobs = fetch_indeed_jobs()
    print("Jobs fetched:", len(jobs))

    # Fallback if empty
    if not jobs:
        print("⚠️ No jobs from Indeed. Using fallback data.")
        jobs = fallback_jobs()

    df = pd.DataFrame(jobs).drop_duplicates()

    print("Columns:", df.columns)

    # Safety check
    if "Title" not in df.columns:
        print("❌ Missing 'Title' column. Exiting safely.")
        return

    # Scoring
    df["Score"] = df["Title"].apply(score_job)

    # Filter good jobs
    df = df[df["Score"] >= 3]

    # Save file
    filename = f"QA_Jobs_{datetime.now().date()}.xlsx"
    df.to_excel(filename, index=False)

    print(f"✅ File saved: {filename}")


if __name__ == "__main__":
    main()
