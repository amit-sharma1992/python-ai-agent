
import pandas as pd


def generate_quality_report(
    missing_df,
    duplicate_df,
    null_df,
    extra_df,
    ai_report="AI analysis not available",
    report_path="reports/data_quality_report.xlsx"
):

    summary_data = {
        "Validation": [
            "Missing Records",
            "Duplicate Rows",
            "Null Records",
            "Extra Records"
        ],

        "Count": [
            len(missing_df),
            len(duplicate_df),
            len(null_df),
            len(extra_df)
        ]
    }

    summary_df = pd.DataFrame(summary_data)

    ai_analysis_df = pd.DataFrame({
        "AI Analysis": [ai_report]
    })

    with pd.ExcelWriter(
        report_path,
        engine="openpyxl"
    ) as writer:

        summary_df.to_excel(
            writer,
            sheet_name="Summary",
            index=False
        )

        missing_df.to_excel(
            writer,
            sheet_name="Missing_Records",
            index=False
        )

        duplicate_df.to_excel(
            writer,
            sheet_name="Duplicate_Records",
            index=False
        )

        null_df.to_excel(
            writer,
            sheet_name="Null_Records",
            index=False
        )

        extra_df.to_excel(
            writer,
            sheet_name="Extra_Records",
            index=False
        )

        ai_analysis_df.to_excel(
            writer,
            sheet_name="AI_Analysis",
            index=False
        )

    print("\nExcel Data Quality Report Generated!")
    print("Report Location:", report_path)
