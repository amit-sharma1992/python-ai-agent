
import pandas as pd


def find_missing_records(source_df, target_df, primary_key):

    missing_records = source_df[
        ~source_df[primary_key].isin(target_df[primary_key])
    ]

    return missing_records
