import requests
import argparse
from github import Github
import github
import time

def wait_for_rate_limit(user, repo, g):
    while g.rate_limiting[0] < 100:
        time.sleep(60)
    getFiletreeForRepo(user, repo, g)

def getFiletreeForRepo(user, repo, g, f):
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
                f.write(path+'\n')
    except github.GithubException as exc:
        print(exc)
        raise

def main():
    parser = argparse.ArgumentParser(description="Script for counting files in github repo")
    parser.add_argument('file_path', help="path to file containing repo urls, one url for each line")
    parser.add_argument('-t', '--token', help='Github token for getting a better rate limit', default=None)
    args = parser.parse_args()

    f = open(args.file_path, 'r')
    lines = f.readlines()
    f.close()
    
    if args.token != None:
        g = Github(args.token)
    else:
        g = Github()

    visited_lines = 0
    with open('github_info.results', 'w') as f:
        try:
            for line in lines:
                url = line.split('/')
                user, repo = url[3:5]
                f.write('#repo:%s/%s \n' % (user, repo))
                getFiletreeForRepo(user, repo, g, f)
                visited_lines += 1
        except github.GithubException as exc:
            f = open(args.file_path, 'w')
            for line in lines[visited_lines:]:
                f.write(line)

if __name__=='__main__':
    main()
