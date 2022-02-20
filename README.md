# github-pull

## A small script for pulling all of your GitHub repositories when setting a up a new machine, because I'm tired of doing it manually.

> **_Note:_** this is designed to pull the first 100 repos a user may have (100 being GitHub's limit before pagination). If you have over 100 repos, then a) you need to get your life together, and b) you can probably do this better than I can.
  

---


_This is designed to work with Unix-based operating systems, and has not been tested on Windows._

## Requirements
- This script assumes you have your machine's SSH key on your GitHub account.

## Steps to run

- Create a virtual environment with `virtualenv` (optional but highly recommended)
- Generate a [GitHub personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) for your GitHub account.
- create an empty file called `.env` in the same folder as your code, and add the following key-value pairs:
```
GITHUB_PAT=yourpersonalaccesstoken123
GITHUB_USERNAME=yourgithubusername
```
- Run `pip install -r requirements.txt` to install the required dependencies.
- Run `python github-pull.py` if executing the file from the root folder you want to clone the repos to. 

Alternative, you can run GitHub-Pull as a command-line tool, as follows:

```python
python github-pull.py --username johnsmith --token abcdef123456 --output /home/username/projects/ --include-orgs 
```

Note that adding a token or username via the command line will override the value stored in the `.env` file
