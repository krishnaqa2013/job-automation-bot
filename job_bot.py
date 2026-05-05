import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

HEADERS = {"User-Agent": "Mozilla/5.0"}


# 🔹 Indeed (structured extraction)
def fetch_indeed_jobs():
    jobs = []

    url = "https://in.indeed.com/jobs?q=QA+Automation+Lead&l=India&fromage=3"

    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        cards = soup.find_all("div", class_="job_seen_beacon")

        for card in cards:
            title_tag = card.find("h2")
            company_tag = card.find("span", class_="companyName")

            if title_tag and company_tag:
                title = title_tag.get_text(strip=True)
                company = company_tag.get_text(strip=True)

                jobs.append({
                    "Title": title,
                    "Company": company,
                    "Source": "Indeed"
                })

    except Exception as e:
        print("Indeed error:", e)

    return jobs


# 🔹 Naukri (basic parsing)
def fetch_naukri_jobs():
    jobs = []

    url = "https://www.naukri.com/qa-automation-lead-jobs-in-india"

    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        cards = soup.find_all("a", class_="title")

        for card in cards[:20]:
            title = card.get_text(strip=True)

            jobs.append({
                "Title": title,
                "Company": "Unknown",
                "Source": "Naukri"
            })

    except Exception as e:
        print("Naukri error:", e)

    return jobs


# 🔹 Fallback (last resort only)
def fallback_jobs():
    return [
        {"Title": "QA Automation Lead Selenium Playwright", "Company": "Fallback", "Source": "Static"}
    ]


# 🔹 Filter
def filter_jobs(df):
    df = df[df["Title"].str.contains("QA|SDET|Automation", case=False)]
    df = df[df["Title"].str.contains("Senior|Lead|Architect|Manager", case=False)]
    df = df[df["Title"].str.contains("Selenium|Playwright|API", case=False)]
    return df


# 🔹 Score
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
    print("🚀 Running V2.1 Job Bot...")

    jobs = []
    jobs += fetch_indeed_jobs()
    jobs += fetch_naukri_jobs()

    print("Fetched total:", len(jobs))

    if not jobs:
        print("⚠️ Using fallback")
        jobs = fallback_jobs()

    df = pd.DataFrame(jobs).drop_duplicates()

    if "Title" not in df.columns:
        print("❌ Missing Title column")
        return

    df = filter_jobs(df)

    if df.empty:
        print("⚠️ No jobs after filtering → fallback")
        df = pd.DataFrame(fallback_jobs())

    df["Score"] = df["Title"].apply(score_job)

    df = df[df["Score"] >= 4]

    df = df.sort_values(by="Score", ascending=False)

    filename = f"QA_Jobs_{datetime.now().date()}.xlsx"
    df.to_excel(filename, index=False)

    print(f"✅ Saved: {filename}")
    print("Final jobs:", len(df))


if __name__ == "__main__":
    main()
