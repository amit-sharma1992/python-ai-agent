
import pandas as pd


def find_duplicate_records(df, primary_key):

    duplicate_records = df[
        df.duplicated(
            subset=[primary_key],
            keep=False
        )
    ]

    return duplicate_records


if __name__ == "__main__":

    target_df = pd.read_csv("data/target_data.csv")

    duplicate_df = find_duplicate_records(
        target_df,
        "TRX_ID"
    )

    print("\nDuplicate Records:")
    print(duplicate_df)

    print("\nTotal Duplicate Rows:", len(duplicate_df))

    print(
        "Total Duplicate Transaction IDs:",
        duplicate_df["TRX_ID"].nunique()
    )
