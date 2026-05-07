import pandas as pd
from datetime import datetime

def main():
    print("🚀 Job bot started")

    # ✅ Static safe sample data
    jobs = [
        {
            "Job Title": "Senior QA Automation Lead - Selenium Playwright",
            "Company": "Tech Mahindra",
            "Portal": "Indeed",
            "Location": "Hyderabad",
            "Hybrid/Remote": "Hybrid",
            "Posted Date": str(datetime.now().date()),
            "Salary (LPA)": "28-40",
            "Apply Link": "https://example.com/job1"
        },
        {
            "Job Title": "SDET Lead API Automation",
            "Company": "Infosys",
            "Portal": "Naukri",
            "Location": "Remote India",
            "Hybrid/Remote": "Remote",
            "Posted Date": str(datetime.now().date()),
            "Salary (LPA)": "25-35",
            "Apply Link": "https://example.com/job2"
        }
    ]

    df = pd.DataFrame(jobs)

    filename = f"QA_Jobs_{datetime.now().date()}.xlsx"

    print("Creating Excel:", filename)

    df.to_excel(filename, index=False)

    print("✅ Excel created successfully")


if __name__ == "__main__":
    main()
