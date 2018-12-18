import requests
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
    getFiletreeForRepo('tk-it', 'web', '84765bc3ad070e51c023308783ef0d07aab14c67')

if __name__=='__main__':
    main()
