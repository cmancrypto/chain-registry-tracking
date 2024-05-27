import pandas as pd

import pull_requests
import email_notifications

cosmos_repo_pulls = pull_requests.RepoPulls("cosmos", "chain-registry")
#dymension_repo_pulls= pull_requests.RepoPulls(github_user="dymensionxyz",github_repo_name="chain-registry")
[new_pulls,existing_pulls,updated_pulls]=cosmos_repo_pulls.main()
#dymension_repo_pulls.main()

str_new_pulls=new_pulls.drop(columns=["html_url"]).to_string()
str_updated_pulls=updated_pulls.to_string()
email_body="\n".join([str_new_pulls,str_updated_pulls])
email_notifications.main("cosmos-registry-updates",email_body,["cmancrypto@outlook.com"])
