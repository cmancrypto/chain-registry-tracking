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
    df = fetch_df_from_json()
    ##add emails column if it doesn't exist already - i.e empty data frame
    if "emails" not in df.columns:
        try:
            df.insert(0, "emails", str)
        except ValueError as e:
            logger.error(e)

    for arg in args.emails:
        if args.remove:
            logger.info(f"dropped {arg}")
            logger.info("args remove")
            df= df[df.emails != arg]


        else:
            print(arg)

            if arg in df["emails"].values:
                logger.info(f"{arg} already in df")
            else:
                df.loc[len(df)]={"emails":arg}

    write_df_to_json(df)
def get_email_json_path()-> str:
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = f"results/email_list.json"
    json_file_path = os.path.join(parent_dir, filename)
    return json_file_path


def fetch_df_from_json() -> pd.DataFrame:
        # Get the path of the parent directory
        file_path = get_email_json_path()
        if os.path.exists(file_path) and os.path.isfile(file_path):
            try:
                df = pd.read_json(file_path)
                logger.info(f" file imported successfully.")
            except pd.errors.EmptyDataError as e:
                df = pd.DataFrame()
                logger.error(f" Empty data frame in json {file_path}: {e}")
            except ValueError as e:
                df = pd.DataFrame()
                logger.error(f" Value error loading data frame from {file_path}: {e}, making a new blank dataframe")

        else:
            logger.debug(f" json file does not exist in the results directory.")
            df = pd.DataFrame()
        return df

def write_df_to_json(df):
    # Get the path of the parent directory
    file_path = get_email_json_path()
    try:
        df.to_json(file_path, index=False)
        logger.info(f"json written file written to :{file_path}")
    except PermissionError as e:
        logger.error(f"Permission error : {e}")
    except IOError as e:
        logger.error(f"IO error : {e}")

main()