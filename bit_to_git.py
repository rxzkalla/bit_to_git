# sourcery skip: remove-str-from-print
import os
import requests
import time
import json

import platform
OS = platform.system()

from github import Github 

# Load settings from JSON file
with open('settings.json') as f:
    settings = json.load(f)

# Bitbucket credentials
USERNAME, PASSWORD, ORGANIZATION = settings['bit_username'], settings['bit_token'], settings['bit_organization']

# GitHub credentials
GITHUB_TOKEN, GITHUB_ORG = settings['github_token'], settings['github_organization']

# Base URL for Bitbucket API
BASE_URL = settings['bit_url']

# URL for getting repositories in the organization
REPO_URL = f'{BASE_URL}/repositories/{ORGANIZATION}'

# Authentication
auth = (USERNAME, PASSWORD)

# Send request to get repositories
repo_paths = []

next_page_url = REPO_URL
while next_page_url:
    response = requests.get(next_page_url, auth=auth)

    # Check if request was successful
    if response.status_code == 200:
        # Extract repository paths
        repositories = response.json()['values']
        repo_paths.extend([repo['links']['html']['href'] for repo in repositories])

        # Check if there is a next page
        next_page_url = response.json().get('next', None)
    else:
        print(f"Failed to retrieve repositories. Status code: {response.status_code}")
        break

repo_count = repo_paths.__len__()

# Print repository count
print("Repository Paths: ", repo_count)

# Initialize GitHub org client
github_org = Github(GITHUB_TOKEN).get_organization(GITHUB_ORG)

# Define the file path to save the output
output_file = 'migration_errors.txt'

# Run the migration process and redirect the output to a file
with open(output_file, 'w') as f:
    for i, repo_path in enumerate(repo_paths):  

        print("\nLooking at : ", repo_path)

        repo_name = repo_path.split("/")[-1]

        current_dir = os.getcwd()
        target_dir = os.path.join(current_dir, f"{repo_name}.git")

        # If directory exists with repo's name remove locally Windows else Linux
        if os.path.exists(target_dir): 
            os.system(f'rmdir /s /q "{repo_name}.git"') if "Win" in OS else os.system(f'rm -r -f "{repo_name}.git"') 

        # Extract the protocol and domain from the repository URL
        domain, path = repo_path.split('://')

        # Insert username and password into the URL
        repo_path = f'{domain}://{USERNAME}:{PASSWORD}@{path}'

        try:
            # Clone the Bitbucket repository
            os.system(f'git clone --mirror {repo_path}')

            os.chdir(f'{repo_name}.git')

            print("Successfully Cloned.")

            print("Creating ", repo_name)
            github_org.create_repo(repo_name, private=True)  # Initialize GitHub repository

            print("Successfully Created Repo in Github.")

            os.system(f'git push --mirror https://{GITHUB_TOKEN}@github.com/{GITHUB_ORG}/{repo_name}')
            os.system(f'git push --tags https://{GITHUB_TOKEN}@github.com/{GITHUB_ORG}/{repo_name}')

            print(f"Successfully Pushed Repo to https://{GITHUB_TOKEN}@github.com/{GITHUB_ORG}/{repo_name}")

        except Exception as e:
            print("Failed ", repo_name)
            print("Error message:", str(e))

            # Write error details to the output file
            f.write(f"Failed migration for repo: {repo_name}\n")
            f.write(f"Error message: {str(e)}\n")


        # Remove the local clone after pushing
        os.chdir('..')  # Move out of the repository directory
        os.system(f'rmdir /s /q "{repo_name}.git"') if "Win" in OS else os.system(f'rm -r -f "{repo_name}.git"') 

        print("Removed local dir - ", repo_name)

        print(f"Finished {i+1}/{repo_count}  --  {repo_name}")
        time.sleep(20)

print("Migration complete!")
