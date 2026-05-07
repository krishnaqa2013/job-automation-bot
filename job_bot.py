import feedparser
import pandas as pd
from datetime import datetime

RSS_FEEDS = [
    {
        "portal": "Indeed",
        "url": "https://in.indeed.com/rss?q=QA+Automation+Lead&l=India&fromage=3"
    },
    {
        "portal": "Indeed",
        "url": "https://in.indeed.com/rss?q=Senior+SDET+Automation&l=India&fromage=3"
    },
    {
        "portal": "Indeed",
        "url": "https://in.indeed.com/rss?q=Test+Automation+Architect+Selenium&l=India&fromage=3"
    }
]


def detect_work_mode(title):
    t = title.lower()

    if "remote" in t:
        return "Remote"

    return "Hybrid"


def estimate_salary(title):
    t = title.lower()

    if "architect" in t:
        return "35-50"

    if "lead" in t:
        return "28-40"

    if "manager" in t:
        return "30-45"

    if "sdet" in t:
        return "25-35"

    return "20-30"


def fetch_jobs():
    jobs = []

    for feed_info in RSS_FEEDS:
        portal = feed_info["portal"]
        url = feed_info["url"]

        feed = feedparser.parse(url)

        for entry in feed.entries:

            title = entry.get("title", "").strip()

            if not title:
                continue

            lower_title = title.lower()

            # Strong filtering
            if not any(x in lower_title for x in [
                "qa", "sdet", "automation"
            ]):
                continue

            if not any(x in lower_title for x in [
                "lead", "senior", "architect", "manager"
            ]):
                continue

            jobs.append({
                "Job Title": title,
                "Company": entry.get("author", "Unknown"),
                "Portal": portal,
                "Location": "Hyderabad / India",
                "Hybrid/Remote": detect_work_mode(title),
                "Posted Date": entry.get("published", ""),
                "Salary (LPA)": estimate_salary(title),
                "Apply Link": entry.get("link", "")
            })

    return jobs


def main():
    print("🚀 Running V4 Job Bot")

    jobs = fetch_jobs()

    print("Fetched jobs:", len(jobs))

    if not jobs:
        print("❌ No jobs fetched")
        return

    df = pd.DataFrame(jobs).drop_duplicates()

    # Sort latest first
    df = df.sort_values(by="Posted Date", ascending=False)

    filename = f"QA_Jobs_{datetime.now().date()}.xlsx"

    with pd.ExcelWriter(filename, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="QA Jobs")

        ws = writer.sheets["QA Jobs"]

        for col in ws.columns:
            max_length = 0
            column = col[0].column_letter

            for cell in col:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass

            adjusted_width = min(max_length + 5, 50)
            ws.column_dimensions[column].width = adjusted_width

    print(f"✅ Saved: {filename}")


if __name__ == "__main__":
    main()
