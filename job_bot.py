import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

SEARCH_URLS = [

    {
        "portal": "Google Jobs",
        "location": "Hyderabad",
        "mode": "Hybrid",
        "url": "https://www.google.com/search?q=QA+Automation+Hyderabad+jobs"
    },

    {
        "portal": "Google Jobs",
        "location": "India",
        "mode": "Remote",
        "url": "https://www.google.com/search?q=SDET+Remote+India+jobs"
    },

    {
        "portal": "Google Jobs",
        "location": "India",
        "mode": "Remote",
        "url": "https://www.google.com/search?q=Playwright+Automation+India+jobs"
    }
]


def estimate_salary(title):

    t = title.lower()

    if "lead" in t:
        return "28-40"

    if "architect" in t:
        return "35-50"

    if "senior" in t:
        return "22-35"

    return "18-30"


def score_job(title):

    score = 0

    t = title.lower()

    if "playwright" in t:
        score += 3

    if "selenium" in t:
        score += 2

    if "api" in t:
        score += 2

    if "automation" in t:
        score += 2

    if "lead" in t:
        score += 1

    return score


def is_relevant(title):

    t = title.lower()

    keywords = [
        "qa",
        "automation",
        "sdet",
        "playwright",
        "selenium",
        "test"
    ]

    return any(k in t for k in keywords)


def fetch_jobs():

    jobs = []

    for source in SEARCH_URLS:

        print("Fetching:", source["url"])

        try:

            response = requests.get(
                source["url"],
                headers=HEADERS,
                timeout=20
            )

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            titles = soup.find_all("h3")

            print("Titles found:", len(titles))

            for t in titles:

                title = t.get_text(strip=True)

                if not title:
                    continue

                if not is_relevant(title):
                    continue

                jobs.append({

                    "Job Title": title,

                    "Company": "Google Search",

                    "Portal": source["portal"],

                    "Location": source["location"],

                    "Hybrid/Remote": source["mode"],

                    "Posted Date": str(
                        datetime.now().date()
                    ),

                    "Salary (LPA)": estimate_salary(title),

                    "Score": score_job(title),

                    "Apply Link": source["url"]
                })

        except Exception as e:

            print("Error:", str(e))

    return jobs


def main():

    print("🚀 Running QA Job Bot V6")

    jobs = fetch_jobs()

    print("Jobs fetched:", len(jobs))

    if not jobs:

        jobs = [{
            "Job Title": "No QA jobs found today",
            "Company": "-",
            "Portal": "-",
            "Location": "-",
            "Hybrid/Remote": "-",
            "Posted Date": str(datetime.now().date()),
            "Salary (LPA)": "-",
            "Score": "-",
            "Apply Link": "-"
        }]

    df = pd.DataFrame(jobs)

    df = df.drop_duplicates(
        subset=["Job Title"]
    )

    if "Score" in df.columns:

        df = df.sort_values(
            by="Score",
            ascending=False
        )

    filename = f"QA_Jobs_{datetime.now().date()}.xlsx"

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

        for col in ws.columns:

            max_length = 0

            column = col[0].column_letter

            for cell in col:

                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass

            ws.column_dimensions[
                column
            ].width = min(
                max_length + 5,
                50
            )

    print("✅ Excel saved:", filename)


if __name__ == "__main__":
    main()
