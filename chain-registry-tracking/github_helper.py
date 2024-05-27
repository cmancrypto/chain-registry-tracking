from github import Github
from github.Repository import Repository
from github import Auth
from dotenv import load_dotenv
import os
from loguru import logger
import pandas as pd
import pandas.errors
from typing import Optional

##helpers to assist with using the Github library

def get_github_instance() -> Github:
    load_dotenv()
    ##this is a GitHub API Fine Grained Access Token
    GITHUB_PERSONAL_ACCESS_TOKEN = os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN")
    if GITHUB_PERSONAL_ACCESS_TOKEN:
        auth = Auth.Token(GITHUB_PERSONAL_ACCESS_TOKEN)
        gh = Github(auth=auth)
        logger.info(f"successfully authenticated as {gh.get_user().login}")
    else:
        gh = Github()
        logger.info(f"no Github personal access token - public repos only")


    return gh


def get_repo(gh_instance: Github, gh_user: str, gh_repo_name: str) -> Repository:
    chain_reg_repo = gh_instance.get_repo(f"{gh_user}/{gh_repo_name}")
    return chain_reg_repo

class RegistryTrackingBase:
    def __init__(self, github_user, github_repo_name,class_type):
        self.github_user = github_user
        self.github_repo_name = github_repo_name
        self.user_repo=f"{self.github_user}-{self.github_repo_name}"
        # instantiate the repo and gitHub objects
        self.gh = get_github_instance()
        self.repo = get_repo(gh_instance=self.gh, gh_user=self.github_user,
                             gh_repo_name=self.github_repo_name)
        self.class_type=class_type

    def get_csv_filepath(self,version: Optional[str] = None):
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if version:
            filename = f"results/{self.github_user}-{self.github_repo_name}-{self.class_type}-{version}.csv"
        else:
            filename = f"results/{self.github_user}-{self.github_repo_name}-{self.class_type}.csv"
        csv_file_path = os.path.join(parent_dir, filename)
        return csv_file_path

    def fetch_df_from_csv(self,**kwargs) -> pd.DataFrame:
        # Get the path of the parent directory

        csv_file_path = self.get_csv_filepath(**kwargs)
        if os.path.exists(csv_file_path) and os.path.isfile(csv_file_path):
            try:
                df = pd.read_csv(csv_file_path)
                logger.info(f"{self.user_repo} CSV file imported successfully.")
            except pandas.errors.EmptyDataError as e:
                df = pd.DataFrame()
                logger.error(f" {self.user_repo} - Empty data frame in CSV {csv_file_path}: {e}")

        else:
            logger.debug(f" {self.user_repo}-{self.class_type} CSV file does not exist in the results directory.")
            df = pd.DataFrame()
        return df

    def write_df_to_csv(self, pull_requests: pd.DataFrame, **kwargs):
        # Get the path of the parent directory
        csv_file_path = self.get_csv_filepath(**kwargs)
        try:
            pull_requests.to_csv(csv_file_path, index=False)
            logger.info(f"{self.user_repo} CSV file successfully written to :{csv_file_path}")
        except PermissionError as e:
            logger.error(f"Permission error : {e}")
        except IOError as e:
            logger.error(f"IO error : {e}")
