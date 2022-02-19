import kirjava
import subprocess
import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_PERSONAL_ACCESS_TOKEN = os.getenv('GITHUB_PAT') # your GitHub Personal Access Token
GITHUB_USERNAME = os.getenv('GITHUB_USERNAME')

client = kirjava.Client(f"https://api.github.com/graphql")
client.headers["Authorization"] = f"bearer {GITHUB_PERSONAL_ACCESS_TOKEN}"

raw_response = client.execute(
    """
    query{
        viewer {
            repositories(first: 100) {
            totalCount
            nodes {
                nameWithOwner
            }
            pageInfo {
                endCursor
                hasNextPage
            }
            }
        }
    }
    """)

repo_list = [n['nameWithOwner'] for n in raw_response['data']['viewer']['repositories']['nodes']]

for r in repo_list:
    if not os.path.exists(r.split("/")[1]):
        if GITHUB_USERNAME in r:
            subprocess.call(["git", "clone", f"git@github.com:{r}.git"])