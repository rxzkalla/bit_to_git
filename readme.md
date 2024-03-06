# Bitbucket to GitHub Migration Tool

This repo is a Python script that migrates a Bitbucket organization's repos to a GitHub organization.

## Dependencies

```bash
pip install PyGithub==2.2.0
```

## Usage

1. Edit ```settings.json``` with your authentication tokens from both Bitbucket and GitHub.
2. Run  ```bit_to_git.py``` to begin migration.
3. Run ``` del_all_git_repos.py ``` to bulk delete all repos in GitHub organization. They will be moved to GitHub's recently deleted repos section if you need to recover them. 
4. It will not work if you try to migrate a repo when GitHub already has a repo with the same name. Either delete the repo(s) manually or run ``` del_all_git_repos.py ``` for quick bulk removal. This makes it easy if you need to remove all repos and restart the migration. 
