import feedparser
import pandas as pd
from datetime import datetime

RSS_FEEDS = [

    # Hyderabad Hybrid
    {
        "portal": "Indeed",
        "location": "Hyderabad",
        "mode": "Hybrid",
        "url": "https://in.indeed.com/rss?q=QA+Automation+Lead+Hyderabad&fromage=3"
    },

    {
        "portal": "Indeed",
        "location": "Hyderabad",
        "mode": "Hybrid",
        "url": "https://in.indeed.com/rss?q=Senior+SDET+Hyderabad&fromage=3"
    },

    # India Remote
    {
        "portal": "Indeed",
        "location": "India",
        "mode": "Remote",
        "url": "https://in.indeed.com/rss?q=Playwright+Automation+Remote+India&fromage=3"
    },

    {
        "portal": "Indeed",
        "location": "India",
        "mode": "Remote",
        "url": "https://in.indeed.com/rss?q=QA+Lead+Remote+India&fromage=3"
    },

    # Abroad Remote
    {
        "portal": "Indeed",
        "location": "Abroad",
        "mode": "Remote",
        "url": "https://www.indeed.com/rss?q=Senior+QA+Automation+Remote&fromage=3"
    }
]


def estimate_salary(title, location):
    t = title.lower()

    if location == "Abroad":
        return "60-100"

    if "architect" in t:
        return "35-50"

    if "lead" in t:
        return "28-40"

    if "manager" in t:
        return "30-45"

    if "sdet" in t:
        return "25-35"

    return "20-30"


def is_relevant(title):
    t = title.lower()

    keywords = [
        "qa",
        "automation",
        "sdet",
        "playwright",
        "selenium",
        "api",
        "test"
    ]

    seniority = [
        "senior",
        "lead",
        "architect",
        "manager"
    ]

    return (
        any(k in t for k in keywords)
        and any(s in t for s in seniority)
    )


def fetch_jobs():
    jobs = []

    for source in RSS_FEEDS:

        print("Fetching:", source["url"])

        feed = feedparser.parse(source["url"])

        for entry in feed.entries:

            title = entry.get("title", "").strip()

            if not title:
                continue

            if not is_relevant(title):
                continue

            jobs.append({
                "Job Title": title,
                "Company": entry.get("author", "Unknown"),
                "Portal": source["portal"],
                "Location": source["location"],
                "Hybrid/Remote": source["mode"],
                "Posted Date": entry.get("published", ""),
                "Salary (LPA)": estimate_salary(
                    title,
                    source["location"]
                ),
                "Apply Link": entry.get("link", "")
            })

    return jobs


def main():

    print("🚀 Running V5 Job Bot")

    jobs = fetch_jobs()

    print("Fetched jobs:", len(jobs))

    # Fallback protection
    if not jobs:

        jobs = [{
            "Job Title": "No matching QA jobs found today",
            "Company": "-",
            "Portal": "-",
            "Location": "-",
            "Hybrid/Remote": "-",
            "Posted Date": str(datetime.now().date()),
            "Salary (LPA)": "-",
            "Apply Link": "-"
        }]

    df = pd.DataFrame(jobs).drop_duplicates()

    filename = f"QA_Jobs_{datetime.now().date()}.xlsx"

    with pd.ExcelWriter(filename, engine="openpyxl") as writer:

        df.to_excel(
            writer,
            index=False,
            sheet_name="QA Jobs"
        )

        ws = writer.sheets["QA Jobs"]

        # Auto width
        for col in ws.columns:

            max_length = 0
            column = col[0].column_letter

            for cell in col:

                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass

            ws.column_dimensions[column].width = min(
                max_length + 5,
                50
            )

    print(f"✅ Saved: {filename}")


if __name__ == "__main__":
    main()
