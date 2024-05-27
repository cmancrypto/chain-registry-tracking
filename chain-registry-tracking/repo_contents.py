from typing import Optional

import github.GithubException
import pandas
from github import Github, Repository
from loguru import logger
from github_helper import get_github_instance, get_repo, RegistryTrackingBase
import os.path
import csv
import pandas as pd

class ContentFilter:
    def __init__(self, name:str, path: str, return_file_content_type : str, recursively_access : bool = False ):
        """
        Content Filter designed to be used with class RepoContents to define parameters needed for the functions in RepoContents
        :param name: name of filter - will be used as {version} for CSV file to not overwrite others of same user/repo/class_type
        :type name: str
        :param path: path of directory in repo to search - "" will search all
        :type path: str
        :param return_file_content_type: type of file to return - example"dir" or "file"
        :type return_file_content_type: str
        :param recursively_access: access dir within dir
        :type recursively_access: bool
        """
        self.name=name
        self.path=path
        self.return_file_content_type=return_file_content_type
        self.recursively_access=recursively_access

class RepoContents(RegistryTrackingBase):
    def __init__(self, github_user, github_repo_name, content_filters : ContentFilter):
        super().__init__(github_user=github_user, github_repo_name=github_repo_name, class_type="repo-contents")
        self.content_filters=content_filters


    def get_path_contents(self) -> list:
        if self.content_filters.path == None: path=""
        try:
            contents = self.repo.get_contents(self.content_filters.path)
        except github.UnknownObjectException as e:
            logger.error(f"No content found at path for {self.github_repo_name}:{e}")
            raise
        return_contents=[]
        while contents:
            file_content=contents.pop(0)
            if file_content.type == self.content_filters.return_file_content_type:
                logger.info(f"got {self.content_filters.return_file_content_type} : {file_content.path}" )
                return_contents.append(file_content)
            if self.content_filters.recursively_access == True and file_content.type =="dir":
                contents.extend(self.repo.get_contents(file_content.path))
                logger.info(f"adding dir {file_content.path} to search")
        return return_contents


    def convert_contents_to_names(self, contents : list):
        converted_contents=[]
        for content in contents:
            converted_contents.append(content.name)
        return converted_contents

    def main(self)->pandas.DataFrame:
        existing_df=self.fetch_df_from_csv(version=self.content_filters.name)
        contents=self.get_path_contents()
        contents_names=self.convert_contents_to_names(contents)
        df=pd.DataFrame({"contents_names" : contents_names})
        self.write_df_to_csv(df,version=self.content_filters.name)
        ## ~ negates the isin operator to get new df contents NOT IN existing df
        new_contents_df=df[~df.iloc[:,0].isin(existing_df.iloc[:,0])]
        return new_contents_df




content_filters=ContentFilter(name="testnets",
                              path="testnets",
                              return_file_content_type="dir",
                              recursively_access=False)

repo_contents=RepoContents("cosmos","chain-registry", content_filters=content_filters)
repo_contents.main()








