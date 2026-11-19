
import pandas as pd


def find_extra_records(source_df, target_df, primary_key):

    extra_records = target_df[
        ~target_df[primary_key].isin(source_df[primary_key])
    ]

    print("\nExtra Records in Target:")

    print(extra_records)

    print("\nTotal Extra Records:", len(extra_records))

    return extra_records


if __name__ == "__main__":

    source_df = pd.read_csv("data/source_data.csv")
    target_df = pd.read_csv("data/target_data.csv")

    find_extra_records(
        source_df,
        target_df,
        "TRX_ID"
    )
