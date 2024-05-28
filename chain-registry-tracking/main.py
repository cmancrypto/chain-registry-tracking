import email_notifications
import repo_contents
from loguru import logger

class RepoContentUpdateNotification():
    def __init__(self,
                 gh_repo_owner: str,
                 gh_repo_name: str,
                 notification_receivers: list,
                 content_filter : repo_contents.ContentFilter
                 ):
        """

        :param gh_repo_owner: gh username that owns the repo to check
        :param gh_repo_name: gh repo  name - combined with owner makes {owner}/{repo_name} i.e. cosmos/chain-registry
        :param notification_receivers: list of email addresses to receive notification
        :param content_filter: filters of type repo_contents.ContentFilter - used to build the content query
        """
        self.gh_repo_owner = gh_repo_owner
        self.gh_repo_name = gh_repo_name
        self.notification_receivers=notification_receivers
        self.content_filter = content_filter

    def main(self):
        repo_contents_instance=repo_contents.RepoContents(self.gh_repo_owner,
                                                          self.gh_repo_name,
                                                          content_filter=self.content_filter)
        new_contents=repo_contents_instance.main()
        count_new=new_contents[new_contents.columns[0]].count()
        logger.info(f"Got {count_new} new {self.content_filter.return_file_content_type} in {self.gh_repo_owner}/{self.gh_repo_name} ")

        if count_new > 0:
            #start to build the email
            message_text=f"""
            Got {count_new} new {self.content_filter.return_file_content_type} 
            in {self.gh_repo_owner}/{self.gh_repo_name}
            at path{self.content_filter.path} : \n
            {new_contents.to_string()}
            """
            message_subject=f"Got {count_new} new {self.content_filter.return_file_content_type} in {self.gh_repo_owner}/{self.gh_repo_name}"
            email_notifications.main(message_subject, message_text, self.notification_receivers)

if __name__=="__main__":
    content_filters = repo_contents.ContentFilter(name="testnets",
                            path="testnets",
                            return_file_content_type="dir",
                            recursively_access=False)
    chain_reg_testnet = RepoContentUpdateNotification("cosmos",
                                  "chain-registry",
                                  ["cmancrpyto@outlook.com"],
                                  content_filter=content_filters)
    chain_reg_testnet.main()

