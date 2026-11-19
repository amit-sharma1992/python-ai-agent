
import pandas as pd


def find_null_values(df):

    null_records = df[df.isnull().any(axis=1)]

    null_summary = df.isnull().sum()

    null_summary = null_summary[null_summary > 0]

    print("\nNull Value Detection Results:")

    print("\nNull Records:")
    print(null_records)

    print("\nNull Count By Column:")
    print(null_summary)

    print("\nTotal Null Values:", int(null_summary.sum()))

    return null_records


if __name__ == "__main__":

    target_df = pd.read_csv("data/target_data.csv")

    find_null_values(target_df)
