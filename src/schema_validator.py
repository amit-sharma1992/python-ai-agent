
import pandas as pd


def validate_schema(source_df, target_df):

    source_columns = set(source_df.columns)
    target_columns = set(target_df.columns)

    missing_columns = source_columns - target_columns
    extra_columns = target_columns - source_columns

    print("\nSchema Validation Results")

    print("\nMissing Columns in Target:")
    print(missing_columns if missing_columns else "None")

    print("\nExtra Columns in Target:")
    print(extra_columns if extra_columns else "None")

    print("\nData Type Mismatches:")

    common_columns = source_columns.intersection(target_columns)

    mismatch_found = False

    for column in sorted(common_columns):

        source_type = str(source_df[column].dtype)
        target_type = str(target_df[column].dtype)

        if source_type != target_type:

            mismatch_found = True

            print(
                f"{column}: Source={source_type}, "
                f"Target={target_type}"
            )

    if not mismatch_found:
        print("None")


if __name__ == "__main__":

    source_df = pd.read_csv("data/source_data.csv")
    target_df = pd.read_csv("data/target_data.csv")

    validate_schema(source_df, target_df)
