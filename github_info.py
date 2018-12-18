import requests
import argparse
from github import Github

def getFiletreeForRepo(user, repo, token):
    filetree = {}
    g = Github(token)
    repo = g.get_repo('{}/{}'.format(user, repo))
    contents = repo.get_contents('')
    while len(contents) > 1:
        file_content = contents.pop(0)
        if file_content.type == 'dir':
            contents.extend(repo.get_contents(file_content.path))
        else:
            path = file_content.path
            print(path)

def main():
    parser = argparse.ArgumentParser(description="Script for counting files in github repo")
    parser.add_argument('file_path', help="path to file containing repo urls, one url for each line")
    args = parser.parse_args()

    repo_to_visit = []
    with open(args.file_path, 'r') as f:
        for line in f:
            url = line.split('/')
            user, repo = url[3:5]
            repo_to_visit.append((user, repo))

    for r in repo_to_visit:
        getFiletreeForRepo(r[0], r[1], '84765bc3ad070e51c023308783ef0d07aab14c67')

if __name__=='__main__':
    main()
