##purpose is to track pull requests, keeps a CSV currently (can extend later to db) and then gets pull requests since the last one in the CSV were made
import pandas.errors
from github import Github, Repository
from loguru import logger
from github_helper import get_github_instance, get_repo, RegistryTrackingBase
import os.path
import csv
import pandas as pd


class RepoPulls(RegistryTrackingBase):
    def __init__(self, github_user, github_repo_name):
        super().__init__(github_user=github_user,github_repo_name=github_repo_name,class_type="pull-requests")


    def main(self) -> list[pandas.DataFrame]:
        # get the existing pulls from csv, if it exists, else get a blank df
        existing_pulls = self.fetch_df_from_csv()
        new_pulls = self.get_new_pulls(chain_registry_repo=self.repo, existing_pulls=existing_pulls)
        combined = pd.concat([existing_pulls, new_pulls])
        self.write_df_to_csv(combined)
        return [new_pulls, existing_pulls]

    def get_new_pulls(self, chain_registry_repo: Repository,
                      existing_pulls: pandas.DataFrame) -> pandas.DataFrame:

        # get the id of the existing latest pull request in the csv
        number = int(existing_pulls["number"].iloc[-1]) + 1 if not existing_pulls.empty else 1
        # get latest pull from repo to check to get our CSV up to date against
        latest_pull = self.get_latest_pull_request_number(chain_registry_repo)
        pulls = []
        while number <= latest_pull:
            try:
                pulls.append(self.get_formatted_pull(chain_registry_repo=chain_registry_repo,pull_number=number))
                number = number + 1
            except KeyboardInterrupt:
                logger.info(f"Keyboard interrupt {self.user_repo} at pull {number}, creating csv")
                break
            except Exception as e:
                logger.error(f"error getting {self.user_repo} pull {number} : {type(e).__name__} with {e} ")
                number = number + 1
        new_pulls = pd.DataFrame(pulls)
        logger.info(f"got {len(pulls)} new PR from {self.user_repo}")
        return new_pulls


    def get_formatted_pull(self,chain_registry_repo: Repository,pull_number):
        pull = chain_registry_repo.get_pull(int(pull_number))
        logger.info(f"got {self.user_repo} PR {pull_number} : {pull.title}")
        formatted_labels = []
        for labels in pull.labels:
            formatted_labels.append(labels.name)
        pull= {"number": pull.number,
                      "label": formatted_labels,
                      "title": pull.title,
                      "created": pull.created_at,
                      "html_url": pull.html_url,
                      "state": pull.state,
                      "merged_at": pull.merged_at}
        return pull

    def get_latest_pull_request_number(self, chain_registry_repo: Repository)->int:
        pulls = chain_registry_repo.get_pulls(sort="created", direction="desc")
        latest_number = pulls[0].number
        return latest_number

    def check_for_updates(self)->list:
        existing_pulls=self.fetch_df_from_csv()
        ##get existing pulls that are not merged AND are either open or missing state
        existing_pulls_filtered=existing_pulls[(existing_pulls["merged_at"].isnull())
                                               & ((existing_pulls["state"]=="open") | (existing_pulls["state"].isna()))]
        numbers = existing_pulls_filtered["number"].tolist()
        return numbers

    def update_pull_requests(self):
        numbers_to_check=self.check_for_updates()
        logger.info(numbers_to_check)
        df=self.fetch_df_from_csv()
        updated_pulls=[]
        for number in numbers_to_check:
            try:
                new_pull=self.get_formatted_pull(chain_registry_repo=self.repo, pull_number=number)
                new_series=pd.Series(new_pull)
                row_index = df.index[df['number'] == new_series['number']].tolist()
                if row_index:
                    if new_series["merged_at"]==None and new_series["state"]=="open":
                        logger.info(f"{df.loc[row_index[0]]['number']} hasn't changed" )
                        pass
                    else:
                        df.loc[row_index[0],:] = pd.Series(new_series)
                        logger.info(f"{df.loc[row_index[0]]['number']} updated with new state/merged data")
                        updated_pulls.append(new_series)
                else:
                    logger.error(f"{row_index} does not exist in dataFrame")
            except KeyboardInterrupt:
                logger.info(f"Keyboard interrupt {self.user_repo} at pull {number}, creating csv")
                break
            except Exception as e:
                logger.error(f"error getting {self.user_repo} pull {number} : {type(e).__name__} with {e} ")
        self.write_df_to_csv(df)
        logger.info(f"{len(updated_pulls)} updated pull requests")
        return updated_pulls



cosmos_repo_pulls = RepoPulls("cosmos", "chain-registry")
dymension_repo_pulls= RepoPulls(github_user="dymensionxyz",github_repo_name="chain-registry")
cosmos_repo_pulls.main()
dymension_repo_pulls.main()
cosmos_repo_pulls.update_pull_requests()
