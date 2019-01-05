import requests
import argparse
from github import Github
import github
import time

def wait_for_rate_limit(user, repo, g):
    while g.rate_limiting[0] < 100:
        time.sleep(60)
    getFiletreeForRepo(user, repo, g)

def getFiletreeForRepo(user, repo, g):
    filetree = {}
    try:
        repo = g.get_repo('{}/{}'.format(user, repo))
        contents = repo.get_contents('')

        while len(contents) > 1:
            file_content = contents.pop(0)
            if file_content.type == 'dir':
                contents.extend(repo.get_contents(file_content.path))
            else:
                path = file_content.path
                print(path)
    except github.GithubException as exc:
        print(exc)
        if isinstance(exc, github.RateLimitExceededException):
            wait_for_rate_limit(user, repo, g)

def main():
    parser = argparse.ArgumentParser(description="Script for counting files in github repo")
    parser.add_argument('file_path', help="path to file containing repo urls, one url for each line")
    parser.add_argument('-t', '--token', help='Github token for getting a better rate limit', default=None)
    args = parser.parse_args()
    
    repo_to_visit = []
    with open(args.file_path, 'r') as f:
        for line in f:
            url = line.split('/')
            user, repo = url[3:5]
            repo_to_visit.append((user, repo))

    if args.token != None:
        g = Github(args.token)
    else:
        g = Github()

    for r in repo_to_visit:
        print('#repo:%s/%s' % (r[0],r[1]))
        getFiletreeForRepo(r[0], r[1], g)

if __name__=='__main__':
    main()
