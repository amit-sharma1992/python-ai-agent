
import pandas as pd

from report_generator import generate_quality_report
from missing_records import find_missing_records
from duplicate_checker import find_duplicate_records
from schema_validator import validate_schema
from null_checker import find_null_values
from extra_records import find_extra_records


def main():

    print("=" * 55)
    print("       AI DATA QUALITY AGENT")
    print("=" * 55)

    # Step 1: Load source and target data
    source_df = pd.read_csv("data/source_data.csv")
    target_df = pd.read_csv("data/target_data.csv")

    print("\nSource Records:", len(source_df))
    print("Target Records:", len(target_df))

    # Step 2: Missing record detection
    print("\n1. MISSING RECORD VALIDATION")

    missing_df = find_missing_records(
        source_df,
        target_df,
        "TRX_ID"
    )

    print(missing_df)
    print("Total Missing Records:", len(missing_df))

    # Step 3: Duplicate detection
    print("\n2. DUPLICATE RECORD VALIDATION")

    duplicate_df = find_duplicate_records(
        target_df,
        "TRX_ID"
    )

    print(duplicate_df)
    print("Total Duplicate Rows:", len(duplicate_df))

    # Step 4: Schema validation
    print("\n3. SCHEMA VALIDATION")

    validate_schema(
        source_df,
        target_df
    )

    # Step 5: Null value detection
    print("\n4. NULL VALUE VALIDATION")

    null_df = find_null_values(target_df)

    # Step 6: Extra record detection
    print("\n5. EXTRA RECORD VALIDATION")

    extra_df = find_extra_records(
        source_df,
        target_df,
        "TRX_ID"
    )

    # Step 7: Generate Excel Report
    generate_quality_report(
        missing_df,
        duplicate_df,
        null_df,
        extra_df
    )

    # Step 8: Final summary
    print("\n" + "=" * 55)
    print("           DATA QUALITY SUMMARY")
    print("=" * 55)

    print("Missing Records:", len(missing_df))
    print("Duplicate Rows:", len(duplicate_df))
    print("Null Records:", len(null_df))
    print("Extra Records:", len(extra_df))

    print("\nData Quality Validation Completed!")


if __name__ == "__main__":
    main()
