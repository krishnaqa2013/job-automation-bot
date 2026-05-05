import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

HEADERS = {"User-Agent": "Mozilla/5.0"}

KEYWORDS = [
    "QA Automation Lead Playwright Selenium India",
    "Senior SDET API Automation India",
    "Test Automation Architect Selenium Java India",
    "QA Automation Manager API Selenium India"
]


# 🔹 Google Jobs (stable source)
def fetch_google_jobs():
    jobs = []

    for keyword in KEYWORDS:
        url = f"https://www.google.com/search?q={keyword.replace(' ', '+')}+jobs"

        try:
            res = requests.get(url, headers=HEADERS, timeout=10)
            soup = BeautifulSoup(res.text, "html.parser")

            for g in soup.select("div"):
                text = g.get_text(" ", strip=True)

                if any(x in text for x in ["QA", "SDET", "Automation"]) and len(text) < 200:
                    jobs.append({
                        "Title": text,
                        "Company": "Unknown",
                        "Source": "Google"
                    })

        except Exception as e:
            print("Error:", e)

    return jobs


# 🔹 Fallback (never fail)
def fallback_jobs():
    return [
        {"Title": "QA Automation Lead Selenium Playwright", "Company": "Fallback", "Source": "Static"},
        {"Title": "Senior SDET API Automation", "Company": "Fallback", "Source": "Static"},
        {"Title": "Test Automation Architect Java Selenium", "Company": "Fallback", "Source": "Static"}
    ]


# 🔹 Strong filtering
def filter_jobs(df):
    df = df[df["Title"].str.contains("QA|SDET|Automation", case=False)]
    df = df[df["Title"].str.contains("Senior|Lead|Architect|Manager", case=False)]
    df = df[df["Title"].str.contains("Selenium|Playwright|API", case=False)]
    return df


# 🔹 Smart scoring
def score_job(title):
    score = 0
    t = title.lower()

    if "playwright" in t: score += 3
    if "selenium" in t: score += 2
    if "api" in t: score += 2
    if "lead" in t or "architect" in t: score += 2
    if "manager" in t: score += 1

    return score


# 🔹 Main
def main():
    print("🚀 Running V2 Job Bot...")

    jobs = fetch_google_jobs()
    print("Fetched:", len(jobs))

    if not jobs:
        print("⚠️ Using fallback data")
        jobs = fallback_jobs()

    df = pd.DataFrame(jobs).drop_duplicates()

    if "Title" not in df.columns:
        print("❌ Missing Title column")
        return

    df = filter_jobs(df)

    if df.empty:
        print("⚠️ No jobs after filtering. Using fallback")
        df = pd.DataFrame(fallback_jobs())

    df["Score"] = df["Title"].apply(score_job)

    df = df[df["Score"] >= 5]

    df = df.sort_values(by="Score", ascending=False)

    filename = f"QA_Jobs_{datetime.now().date()}.xlsx"
    df.to_excel(filename, index=False)

    print(f"✅ Saved: {filename}")
    print(f"Final jobs count: {len(df)}")


if __name__ == "__main__":
    main()
