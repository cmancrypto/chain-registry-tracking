import argparse
import os
import pandas as pd
from loguru import logger
##this is the CLI Interface for the email registration


def main():
    # Initialize parser
    parser = argparse.ArgumentParser()

    # Adding optional argument
    parser.add_argument("emails", help="Email Addresses to add", nargs="+")
    parser.add_argument("-r", "--remove", action="store_true", help="remove email address")

    # Read arguments from command line
    args = parser.parse_args()

    for arg in args.emails:
        if args.remove:
        #remove logic
        else:
        #add logic

def get_email_json_path()-> str:
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = f"results/email_list.json"
    csv_file_path = os.path.join(parent_dir, filename)
    return csv_file_path


def fetch_df_from_json() -> pd.DataFrame:
        # Get the path of the parent directory
        file_path = get_email_json_path()
        if os.path.exists(file_path) and os.path.isfile(file_path):
            try:
                df = pd.read_csv(file_path)
                logger.info(f" file imported successfully.")
            except pd.errors.EmptyDataError as e:
                df = pd.DataFrame()
                logger.error(f" Empty data frame in json {file_path}: {e}")

        else:
            logger.debug(f" json file does not exist in the results directory.")
            df = pd.DataFrame()
        return df