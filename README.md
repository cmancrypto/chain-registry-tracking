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

Notification set to send difference between results folder and most recent run as an email.
Email list comes from file made by email_address_registration.py

Below example from main.py(): 

Will store the dirs names in a CSV and notify by email of changes in sub-directories in the testnets directory of the chain-registry repo since last update of the CSV . 

~~~
    email_list=email_address_registration.get_email_list()
    
    chain_registry_content_filters = repo_contents.ContentFilter(name="testnets",
                                                  path="testnets",
                                                  return_file_content_type="dir",
                                                  recursively_access=False)
                                                  
    chain_reg_testnet = RepoContentUpdateNotification("cosmos",
                                                      "chain-registry",
                                                      email_list,
                                                      content_filter=chain_registry_content_filters)
    chain_reg_testnet.main()
~~~

#   email_address_registration.py 

CLI for saving email addresses to a json file
results/email_list.json

Usage for cli to register email address is: 
~~~
python chain-registry-tracking/email_address_registration.py  email1 email2 emailn
~~~

Use the -r flag to remove email addresses that are registered: 
~~~
python chain-registry-tracking/email_address_registration.py -r email1 email2 emailn
~~~

