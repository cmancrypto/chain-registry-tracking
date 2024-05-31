# chain-registry-tracking
 Tools to track changes on Cosmos Chain Registry

To get started:
~~~
- pip install -r requirements.txt 
~~~

Once all packages installed, edit .env.sample and save as .env 

Tools can be used stand alone or as part of "main.py" which is set up for Chain Registry analysis. 

Tools as below:

repo_contents - tools to scrape directories/files in a repo and save to a CSV 

pull_requests - works, but not finished properly -  tools to scrape pull requests and saves to a CSV

# main.py 
Used to notify of new dirs/files added to GitHub to track changes in Chain Registry. 
Running will save csv's into results folder

Notification set to send difference between results folder and most recent run as an email 

Below example from main.py(): 

Will store the dirs names in a CSV and notify by email of changes in sub-directories in the testnets directory of the chain-registry repo since last update of the CSV . 

~~~
    chain_registry_content_filters = repo_contents.ContentFilter(name="testnets",
                                                  path="testnets",
                                                  return_file_content_type="dir",
                                                  recursively_access=False)
    chain_reg_testnet = RepoContentUpdateNotification("cosmos",
                                                      "chain-registry",
                                                      ["cmancrypto@outlook.com"],
                                                      content_filter=chain_registry_content_filters)
    chain_reg_testnet.main()
~~~

#todo - update to take in email list rather than hard coded email 