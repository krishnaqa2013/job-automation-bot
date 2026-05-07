import requests
import pandas as pd
import os
from datetime import datetime

# ---------------------------------------------------
# APIFY TOKEN
# ---------------------------------------------------

APIFY_TOKEN = os.getenv("APIFY_TOKEN")

# ---------------------------------------------------
# TASK IDS
# ---------------------------------------------------

LINKEDIN_TASK = "a_krishnaqa/linkedin-qa-jobs"

NAUKRI_TASK = "a_krishnaqa/naukri-qa-jobs"

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
# RUN TASK
# ---------------------------------------------------

def run_task(task_id):

    print(f"\n🚀 Running Task: {task_id}")

    url = f"https://api.apify.com/v2/actor-tasks/{task_id}/run-sync-get-dataset-items?token={APIFY_TOKEN}"

    response = requests.post(url)

    print("Status Code:", response.status_code)

    try:

        data = response.json()

    except:

        print("❌ Failed JSON")

        return []

    print("Items Returned:", len(data))

    if len(data) > 0:

        print("Sample Item:")
        print(data[0])

    return data

# ---------------------------------------------------
# FETCH LINKEDIN JOBS
# ---------------------------------------------------

def fetch_linkedin_jobs():

    jobs = run_task(LINKEDIN_TASK)

    formatted = []

    for j in jobs:

        title = str(
            j.get("title", "")
        )

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
# FETCH NAUKRI JOBS
# ---------------------------------------------------

def fetch_naukri_jobs():

    jobs = run_task(NAUKRI_TASK)

    formatted = []

    for j in jobs:

        title = str(
            j.get("title", "")
        )

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

    print("🚀 Running APIFY TASK QA JOB BOT")

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

    # ---------------------------------------------------
    # FALLBACK
    # ---------------------------------------------------

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

    # ---------------------------------------------------
    # DATAFRAME
    # ---------------------------------------------------

    df = pd.DataFrame(all_jobs)

    df = df.drop_duplicates(
        subset=["Job Title", "Company"]
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

    print(f"\n✅ Excel Saved: {filename}")

# ---------------------------------------------------
# START
# ---------------------------------------------------

if __name__ == "__main__":
    main()
