def main():
    print("🚀 Running V4 Job Bot")

    jobs = fetch_jobs()

    print("Fetched jobs:", len(jobs))

    # ✅ Create fallback row if empty
    if not jobs:
        jobs = [{
            "Job Title": "No matching jobs found today",
            "Company": "-",
            "Portal": "-",
            "Location": "India",
            "Hybrid/Remote": "-",
            "Posted Date": str(datetime.now().date()),
            "Salary (LPA)": "-",
            "Apply Link": "-"
        }]

    df = pd.DataFrame(jobs).drop_duplicates()

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

            ws.column_dimensions[column].width = min(max_length + 5, 50)

    print(f"✅ Saved: {filename}")
