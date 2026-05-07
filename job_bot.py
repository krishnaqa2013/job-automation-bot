def main():

    print("🚀 Running APIFY QA JOB BOT")

    all_jobs = []

    # ---------------------------------------------------
    # LINKEDIN DEBUG
    # ---------------------------------------------------

    try:

        linkedin_jobs = fetch_linkedin_jobs()

        print("LinkedIn Raw Output:")
        print(linkedin_jobs)

        print("LinkedIn Jobs Count:", len(linkedin_jobs))

        all_jobs.extend(linkedin_jobs)

    except Exception as e:

        print("LinkedIn Error:", str(e))

    # ---------------------------------------------------
    # NAUKRI DEBUG
    # ---------------------------------------------------

    try:

        naukri_jobs = fetch_naukri_jobs()

        print("Naukri Raw Output:")
        print(naukri
