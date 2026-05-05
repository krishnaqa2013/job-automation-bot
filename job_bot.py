import feedparser
import pandas as pd
from datetime import datetime

# 🔹 RSS URLs (last 3 days filter built-in)
RSS_FEEDS = [
    "https://in.indeed.com/rss?q=QA+Automation+Lead&l=India&fromage=3",
    "https://in.indeed.com/rss?q=Senior+SDET+Automation&l=India&fromage=3",
    "https://in.indeed.com/rss?q=Test+Automation+Architect&l=India&fromage=3"
]


# 🔹 Fetch jobs from RSS
def fetch_jobs():
    jobs = []

    for url in RSS_FEEDS:
        feed = feedparser.parse(url)

        for entry in feed.entries:
            jobs.append({
                "Title": entry.title,
                "Company": entry.get("author", "Unknown"),
                "Link": entry.link,
                "Published": entry.get("published", ""),
                "Source": "Indeed RSS"
            })

    return jobs


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
    print("🚀 Running V3 Job Bot (RSS Mode)...")

    jobs = fetch_jobs()
    print("Fetched:", len(jobs))

    if not jobs:
        print("❌ No jobs fetched")
        return

    df = pd.DataFrame(jobs).drop_duplicates()

    df = filter_jobs(df)

    if df.empty:
        print("⚠️ No jobs after filtering")
        return

    df["Score"] = df["Title"].apply(score_job)

    df = df[df["Score"] >= 4]

    df = df.sort_values(by="Score", ascending=False)

    filename = f"QA_Jobs_{datetime.now().date()}.xlsx"
    df.to_excel(filename, index=False)

    print(f"✅ Saved: {filename}")
    print("Final jobs:", len(df))


if __name__ == "__main__":
    main()
