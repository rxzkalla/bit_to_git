# Deleting Repos
import requests

import json

# Load settings from JSON file
with open('settings.json') as f:
    settings = json.load(f)

# GitHub organization name
ORGANIZATION = settings['github_organization']

# Personal access token
TOKEN =  settings['github_token']

# Base URL for GitHub API
BASE_URL =  settings['github_url']

# Get list of repositories in the organization
url = f'{BASE_URL}/orgs/{ORGANIZATION}/repos'
headers = {
    'Authorization': f'token {TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}
response = requests.get(url, headers=headers)
repositories = response.json()

# Delete repositories
for repo in repositories:
    repo_name = repo['name']
    repo_url = f'{BASE_URL}/repos/{ORGANIZATION}/{repo_name}'
    response = requests.delete(repo_url, headers=headers)
    if response.status_code == 204:
        print(f"Repository '{repo_name}' deleted successfully.")
    else:
        print(f"Failed to delete repository '{repo_name}'. Status code: {response.status_code}")
