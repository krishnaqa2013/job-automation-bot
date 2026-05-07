import pandas as pd
from datetime import datetime

jobs = [
    {
        "Job Title": "Senior QA Automation Lead",
        "Company": "Infosys",
        "Portal": "Indeed",
        "Location": "Hyderabad",
        "Hybrid/Remote": "Hybrid",
        "Posted Date": str(datetime.now().date()),
        "Salary (LPA)": "28-40",
        "Apply Link": "https://example.com/job1"
    },
    {
        "Job Title": "SDET Lead API Automation",
        "Company": "Tech Mahindra",
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

df.to_excel(filename, index=False)

print("✅ Excel created:", filename)
