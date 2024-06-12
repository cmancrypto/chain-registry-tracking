import email_notifications
import email_address_registration
import repo_contents
from loguru import logger


class RepoContentUpdateNotification:
    def __init__(self,
                 gh_repo_owner: str,
                 gh_repo_name: str,
                 notification_receivers: list,
                 content_filter: repo_contents.ContentFilter
                 ):
        """
        Class - purpose of which is to instantiate an object with which to check a specific repo for updates
        then sends a list of the updated blobs/dirs to an email address list.
        Allows for specifying whether to return blobs/dirs, to check dirs in dirs etc. via content_filter

        :param gh_repo_owner: gh username that owns the repo to check
        :param gh_repo_name: gh repo  name - combined with owner makes {owner}/{repo_name} i.e. cosmos/chain-registry
        :param notification_receivers: list of email addresses to receive notification
        :param content_filter: filters of type repo_contents.ContentFilter - used to build the content query
        """
        self.gh_repo_owner = gh_repo_owner
        self.gh_repo_name = gh_repo_name
        self.notification_receivers = notification_receivers
        self.content_filter = content_filter

    def main(self):
        """
        main function to send the notification of a repo update with new files/dirs

        :return:
        """
        repo_contents_instance = repo_contents.RepoContents(self.gh_repo_owner,
                                                            self.gh_repo_name,
                                                            content_filter=self.content_filter)
        new_contents = repo_contents_instance.main()
        count_new = new_contents[new_contents.columns[0]].count()
        logger.info(
            f"Got {count_new} new {self.content_filter.return_file_content_type}"
            f"in {self.gh_repo_owner}/{self.gh_repo_name} ")

        if count_new > 0:
            #start to build the email
            #text is split over multiple lines because displayed badly, didn't use multiline comment since it made the email multiline
            message_text = (f"Got {count_new} new {self.content_filter.return_file_content_type}"
                            f" in {self.gh_repo_owner}/{self.gh_repo_name} at path {self.content_filter.path} "
                            f":\n{new_contents.to_string(index=False,header=False)}")
            message_subject = f"Got {count_new} new {self.content_filter.return_file_content_type} in {self.gh_repo_owner}/{self.gh_repo_name}"
            email_notifications.main(message_subject, message_text, self.notification_receivers)


if __name__ == "__main__":
    email_list=email_address_registration.get_email_list()

    if len(email_list)==0:
        logger.info("No emails in email list - create results/email_list.json first using email_address_registration.py CLI")


    chain_registry_content_filters = repo_contents.ContentFilter(name="testnets",
                                                  path="testnets",
                                                  return_file_content_type="dir",
                                                  recursively_access=False)
    chain_reg_testnet = RepoContentUpdateNotification("cosmos",
                                                      "chain-registry",
                                                      notification_receivers=email_list,
                                                      content_filter=chain_registry_content_filters)
    chain_reg_testnet.main()

    chain_registry_content_filters = repo_contents.ContentFilter(name="mainnets",
                                                  path="",
                                                  return_file_content_type="dir",
                                                  recursively_access=False)
    chain_reg_mainnet = RepoContentUpdateNotification("cosmos",
                                                      "chain-registry",
                                                      notification_receivers=email_list,
                                                      content_filter=chain_registry_content_filters)
    chain_reg_mainnet.main()

    """
    #Example of a recursive search below 
    dym_content_filters = repo_contents.ContentFilter(name="testnets_recursive",
                                                  path="testnet",
                                                  return_file_content_type="file",
                                                  recursively_access=True)
    dym_reg_testnet = RepoContentUpdateNotification("dymensionxyz",
                                                      "chain-registry",
                                                      email_list,
                                                      content_filter=dym_content_filters)
    dym_reg_testnet.main()
    """