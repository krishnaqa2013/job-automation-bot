import requests
import pandas as pd
import os
from datetime import datetime
import time

# ---------------------------------------------------
# APIFY TOKEN
# ---------------------------------------------------

APIFY_TOKEN = os.getenv("APIFY_TOKEN")

# ---------------------------------------------------
# ACTORS
# ---------------------------------------------------

LINKEDIN_ACTOR = "curious_coder/linkedin-jobs-scraper"
NAUKRI_ACTOR = "automation-lab/naukri-scraper"

# ---------------------------------------------------
# SCORING
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

    if "automation" in t:
        score += 2

    if "lead" in t:
        score += 1

    return score

# ---------------------------------------------------
# SALARY ESTIMATION
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

    return "18-30"

# ---------------------------------------------------
# RUN APIFY ACTOR
# ---------------------------------------------------

def run_actor(actor_id, payload):

    url = f"https://api.apify.com/v2/acts/{actor_id}/runs?token={APIFY_TOKEN}"

    response = requests.post(
        url,
        json=payload
    )

    run = response.json()

    run_id = run["data"]["id"]

    print("Run ID:", run_id)

    # Wait for completion
    while True:

        status_url = f"https://api.apify.com/v2/actor-runs/{run_id}?token={APIFY_TOKEN}"

        status_response = requests.get(status_url)

        status_data = status_response.json()

        status = status_data["data"]["status"]

        print("Status:", status)

        if status == "SUCCEEDED":
            break

        if status in ["FAILED", "ABORTED", "TIMED-OUT"]:
            return []

        time.sleep(15)

    dataset_id = status_data["data"]["defaultDatasetId"]

    dataset_url = f"https://api.apify.com/v2/datasets/{dataset_id}/items?clean=true"

    dataset_response = requests.get(dataset_url)

    return dataset_response.json()

# ---------------------------------------------------
# LINKEDIN JOBS
# ---------------------------------------------------

def fetch_linkedin_jobs():

    payload = {
        "urls": [
            "https://www.linkedin.com/jobs/search/?keywords=QA+Automation+Lead&location=Hyderabad%2C+Telangana%2C+India",
            "https://www.linkedin.com/jobs/search/?keywords=SDET+Remote+India",
            "https://www.linkedin.com/jobs/search/?keywords=Playwright+Automation+India"
        ],
        "count": 15
    }

    jobs = run_actor(
        LINKEDIN_ACTOR,
        payload
    )

    formatted = []

    for j in jobs:

        title = j.get("title", "")

        if not title:
            continue

        formatted.append({

            "Job Title": title,

            "Company": j.get(
                "companyName",
                "Unknown"
            ),

            "Portal": "LinkedIn",

            "Location": j.get(
                "location",
                ""
            ),

            "Hybrid/Remote": "Remote"
            if "remote" in str(
                j.get("location", "")
            ).lower()
            else "Hybrid",

            "Posted Date": j.get(
                "postedTime",
                ""
            ),

            "Salary (LPA)": estimate_salary(
                title
            ),

            "Score": score_job(title),

            "Apply Link": j.get(
                "jobUrl",
                ""
            )
        })

    return formatted

# ---------------------------------------------------
# NAUKRI JOBS
# ---------------------------------------------------

def fetch_naukri_jobs():

    payload = {
        "keyword": "QA Automation Selenium Playwright",
        "location": "hyderabad",
        "experienceMin": 8,
        "maxJobs": 15,
        "sortBy": "date"
    }

    jobs = run_actor(
        NAUKRI_ACTOR,
        payload
    )

    formatted = []

    for j in jobs:

        title = j.get("title", "")

        if not title:
            continue

        formatted.append({

            "Job Title": title,

            "Company": j.get(
                "company",
                "Unknown"
            ),

            "Portal": "Naukri",

            "Location": j.get(
                "location",
                ""
            ),

            "Hybrid/Remote": "Hybrid",

            "Posted Date": j.get(
                "date",
                ""
            ),

            "Salary (LPA)": estimate_salary(
                title
            ),

            "Score": score_job(title),

            "Apply Link": j.get(
                "url",
                ""
            )
        })

    return formatted

# ---------------------------------------------------
# MAIN
# ---------------------------------------------------

def main():

    print("🚀 Running APIFY QA JOB BOT")

    all_jobs = []

    # LinkedIn
    try:
        linkedin_jobs = fetch_linkedin_jobs()
        print("LinkedIn Jobs:", len(linkedin_jobs))
        all_jobs.extend(linkedin_jobs)

    except Exception as e:
        print("LinkedIn Error:", str(e))

    # Naukri
    try:
        naukri_jobs = fetch_naukri_jobs()
        print("Naukri Jobs:", len(naukri_jobs))
        all_jobs.extend(naukri_jobs)

    except Exception as e:
        print("Naukri Error:", str(e))

    # Fallback
    if not all_jobs:

        all_jobs = [{
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

    df = pd.DataFrame(all_jobs)

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

    print("✅ Excel Saved:", filename)

if __name__ == "__main__":
    main()
