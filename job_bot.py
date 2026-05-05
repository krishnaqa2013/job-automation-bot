import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta

KEYWORDS = [
    "QA Automation Lead Playwright Selenium",
    "Senior QA Automation Engineer API BDD",
    "SDET Lead API Automation",
    "Test Automation Architect Selenium Java"
]

HEADERS = {"User-Agent": "Mozilla/5.0"}

def fetch_indeed_jobs():
    jobs = []
    for keyword in KEYWORDS:
        url = f"https://in.indeed.com/jobs?q={keyword}&l=India&fromage=3"
        res = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(res.text, "html.parser")

        for card in soup.select(".job_seen_beacon"):
            title = card.select_one("h2").text.strip()
            company = card.select_one(".companyName").text.strip()
            location = card.select_one(".companyLocation").text.strip()

            jobs.append({
                "Title": title,
                "Company": company,
                "Location": location,
                "Source": "Indeed"
            })
    return jobs

def score_job(title):
    score = 0
    title_lower = title.lower()

    if "playwright" in title_lower or "selenium" in title_lower:
        score += 3
    if "api" in title_lower:
        score += 2
    if "lead" in title_lower or "architect" in title_lower:
        score += 2

    return score

def main():
    jobs = fetch_indeed_jobs()

    df = pd.DataFrame(jobs).drop_duplicates()

    df["Score"] = df["Title"].apply(score_job)

    df = df[df["Score"] >= 4]

    filename = f"QA_Jobs_{datetime.now().date()}.xlsx"
    df.to_excel(filename, index=False)

    print(f"Saved: {filename}")

if __name__ == "__main__":
    main()
