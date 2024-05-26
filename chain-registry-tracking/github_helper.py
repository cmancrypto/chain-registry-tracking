from github import Github, Repository
from github import Auth
from dotenv import load_dotenv
import os
from loguru import logger

##helpers to assist with using the Github library

def get_github_instance() -> Github:
    load_dotenv()
    ##this is a GitHub API Fine Grained Access Token
    GITHUB_PERSONAL_ACCESS_TOKEN = os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN")
    auth = Auth.Token(GITHUB_PERSONAL_ACCESS_TOKEN)
    gh = Github(auth=auth)
    logger.info(f"successfully authenticated as {gh.get_user().login}")
    return gh


def get_chain_registry_repo(gh_instance: Github, gh_user: str, gh_repo_name: str) -> Repository:
    chain_reg_repo = gh_instance.get_repo(f"{gh_user}/{gh_repo_name}")
    return chain_reg_repo

