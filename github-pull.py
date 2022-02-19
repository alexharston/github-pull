import kirjava
import subprocess
import os
from dotenv import load_dotenv
from tqdm import tqdm
from rich import print
from rich.padding import Padding
import argparse


load_dotenv()

parser = argparse.ArgumentParser(description='Pull all your repositories from GitHub')

parser.add_argument("-u", "--username", type=str, 
                    help="The GitHub username to pull from.")
parser.add_argument("-t", "--token", type=str, 
                    help="The GitHub personal access token to use.")
parser.add_argument("-o", "--output", type=str, 
                    help="Output path to clone repositories into.")
parser.add_argument("--include-orgs", dest='include_orgs', action='store_true', 
                    help="Also pull repositories from organisations \
                    you are a member of, if any exist. Otherwise just pull your personal repositories.")


args = parser.parse_args()

if args.token:
    GITHUB_PERSONAL_ACCESS_TOKEN = args.token
else:
    try:
        GITHUB_PERSONAL_ACCESS_TOKEN = os.getenv('GITHUB_PAT')
    except:
        raise FileNotFoundError("No GitHub personal access token found. Please provide one with the -t flag, or via a .env file.")
        exit()

if args.username:
    GITHUB_USERNAME = args.username
else:
    try:
        GITHUB_USERNAME = os.getenv('GITHUB_USERNAME')
    except:
        raise FileNotFoundError("No GitHub username found. Please provide one with the -u flag, or via a .env file.")
        exit()

client = kirjava.Client(f"https://api.github.com/graphql")
client.headers["Authorization"] = f"bearer {GITHUB_PERSONAL_ACCESS_TOKEN}"

repos = client.execute(
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

try:
    total_count = repos['data']['viewer']['repositories']['totalCount']
except KeyError:
    print("Error: Could not get total count of repositories. Have you provided a username and token, and does the token have the correct permissions?")
    exit()
print(f"You have {total_count} total repositories to pull")

repo_list = [n['nameWithOwner'] for n in repos['data']['viewer']['repositories']['nodes']]


if args.output:
    directory = str(args.output)
    if not os.path.exists(directory):
        os.makedirs(directory)
    print('Working directory is: ', directory)
else:
    directory = os.getcwd()
    print('Working directory is: ', directory)

print(type(args.username))

if __name__ == "__main__":
    print('Pulling repositories...')
    for r in tqdm(repo_list):
        if args.include_orgs:
            if not os.path.exists(r.split("/")[1]):
                test = Padding(f"[bold magenta]{r}[/bold magenta]", (2, 4))
                print(test)
                subprocess.call(["git", "clone", f"git@github.com:{r}.git"], cwd=directory)
            else:
                print(f"{r} already exists in this directory")
        else:
            if GITHUB_USERNAME in r:
                if not os.path.exists(r.split("/")[1]):
                    test = Padding(f"[bold magenta]{r}[/bold magenta]", (2, 4))
                    print(test)
                    subprocess.call(["git", "clone", f"git@github.com:{r}.git"], cwd=directory)
                else:
                    print(f"{r} already exists in this directory")