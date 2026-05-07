import feedparser
import pandas as pd
from datetime import datetime

# ---------------------------------------------------
# RSS FEEDS
# ---------------------------------------------------

RSS_FEEDS = [

    # Hyderabad Hybrid Jobs
    {
        "portal": "Indeed",
        "location": "Hyderabad",
        "mode": "Hybrid",
        "url": "https://in.indeed.com/rss?q=QA+Automation+Hyderabad&fromage=3"
    },

    {
        "portal": "Indeed",
        "location": "Hyderabad",
        "mode": "Hybrid",
        "url": "https://in.indeed.com/rss?q=SDET+Hyderabad&fromage=3"
    },

    # India Remote Jobs
    {
        "portal": "Indeed",
        "location": "India",
        "mode": "Remote",
        "url": "https://in.indeed.com/rss?q=QA+Automation+Remote+India&fromage=3"
    },

    {
        "portal": "Indeed",
        "location": "India",
        "mode": "Remote",
        "url": "https://in.indeed.com/rss?q=Playwright+Automation+India&fromage=3"
    },

    {
        "portal": "Indeed",
        "location": "India",
        "mode": "Remote",
        "url": "https://in.indeed.com/rss?q=QA+Lead+Remote&fromage=3"
    }
]


# ---------------------------------------------------
# FILTER RELEVANT JOBS
# ---------------------------------------------------

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

    return any(k in t for k in keywords)


# ---------------------------------------------------
# ESTIMATE SALARY
# ---------------------------------------------------

def estimate_salary(title):

    t = title.lower()

    if "architect" in t:
        return "35-50"

    if "lead" in t:
        return "28-40"

    if "manager" in t:
        return "30-45"

    if "senior" in t:
        return "22-35"

    if "sdet" in t:
        return "25-35"

    return "18-30"


# ---------------------------------------------------
# SCORE JOB
# ---------------------------------------------------

def score_job(title):

    score = 0

    t = title.lower()

    if "playwright" in t:
        score += 3

    if "selenium" in t:
        score += 2

    if "api" in t:
        score += 2

    if "lead" in t:
        score += 2

    if "automation" in t:
        score += 1

    return score


# ---------------------------------------------------
# FETCH JOBS
# ---------------------------------------------------

def fetch_jobs():

    jobs = []

    for source in RSS_FEEDS:

        print("Fetching:", source["url"])

        feed = feedparser.parse(source["url"])

        print("Entries found:", len(feed.entries))

        for entry in feed.entries:

            title = entry.get("title", "").strip()

            if not title:
                continue

            if not is_relevant(title):
                continue

            jobs.append({

                "Job Title": title,

                "Company": entry.get(
                    "author",
                    "Unknown"
                ),

                "Portal": source["portal"],

                "Location": source["location"],

                "Hybrid/Remote": source["mode"],

                "Posted Date": entry.get(
                    "published",
                    ""
                ),

                "Salary (LPA)": estimate_salary(title),

                "Score": score_job(title),

                "Apply Link": entry.get(
                    "link",
                    ""
                )
            })

    return jobs


# ---------------------------------------------------
# MAIN
# ---------------------------------------------------

def main():

    print("🚀 Running QA Job Bot V5")

    jobs = fetch_jobs()

    print("Total jobs fetched:", len(jobs))

    # ---------------------------------------------------
    # FALLBACK
    # ---------------------------------------------------

    if not jobs:

        jobs = [{
            "Job Title": "No matching QA jobs found today",
            "Company": "-",
            "Portal": "-",
            "Location": "-",
            "Hybrid/Remote": "-",
            "Posted Date": str(datetime.now().date()),
            "Salary (LPA)": "-",
            "Score": "-",
            "Apply Link": "-"
        }]

    # ---------------------------------------------------
    # DATAFRAME
    # ---------------------------------------------------

    df = pd.DataFrame(jobs)

    # Remove duplicates
    df = df.drop_duplicates(
        subset=["Job Title", "Company"]
    )

    # Sort by score
    if "Score" in df.columns:
        df = df.sort_values(
            by="Score",
            ascending=False
        )

    filename = f"QA_Jobs_{datetime.now().date()}.xlsx"

    # ---------------------------------------------------
    # EXCEL EXPORT
    # ---------------------------------------------------

    with pd.ExcelWriter(
        filename,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            index=False,
            sheet_name="QA Jobs"
        )

        ws = writer.sheets["QA Jobs"]

        # Auto-width columns
        for col in ws.columns:

            max_length = 0

            column = col[0].column_letter

            for cell in col:

                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass

            adjusted_width = min(
                max_length + 5,
                50
            )

            ws.column_dimensions[
                column
            ].width = adjusted_width

    print(f"✅ Excel saved: {filename}")


# ---------------------------------------------------
# START
# ---------------------------------------------------

if __name__ == "__main__":
    main()
