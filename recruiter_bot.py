import pandas as pd
import re

# 🔹 Simple email extractor (from text if available)
def extract_emails(text):
    if not isinstance(text, str):
        return []
    return re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)


# 🔹 Generate recruiter-style message
def generate_message(job_title, company):
    return f"""Hi Hiring Team,

I recently came across the {job_title} role at {company}.

I bring 12+ years of experience in QA Automation (Selenium, Playwright, API testing) and currently work as a QA Lead.

I’m very interested in this opportunity and would appreciate if you could consider my profile.

Happy to share my resume.

Thanks,
Phani Krishna
"""


def main():
    try:
        jobs_file = sorted([f for f in pd.io.common.os.listdir() if f.startswith("QA_Jobs_")])[-1]
    except:
        print("❌ No job file found")
        return

    df = pd.read_excel(jobs_file)

    rows = []

    for _, row in df.iterrows():
        company = row.get("Company", "Unknown")
        title = row.get("Title", "QA Role")

        message = generate_message(title, company)

        rows.append({
            "Company": company,
            "Job Title": title,
            "Suggested Email": f"careers@{company.lower().replace(' ', '')}.com",
            "Message": message
        })

    out_df = pd.DataFrame(rows).drop_duplicates()

    filename = "recruiter_report.xlsx"
    out_df.to_excel(filename, index=False)

    print(f"✅ Recruiter report generated: {filename}")


if __name__ == "__main__":
    main()