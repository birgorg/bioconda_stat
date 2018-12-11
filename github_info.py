import requests

def print_filetree(user, repo, sha, path='/'):
    r = requests.get('https://api.github.com/repos/{}/{}/git/trees/{}'.format(user,repo,sha))
    for f in r.json().get('tree'):
        if f.get('type')=='tree':
            print_filetree(user, repo, f.get('sha'), path+f.get('path')+'/')
        else:
            print(path+f.get('path'))

def getFiletreeOfLastCommit(url):
    user = url.split('/')[-2]
    repo = url.split('/')[-1]
    print(user)
    print(repo)
    r = requests.get('https://api.github.com/repos/{}/{}/commits'.format(user,repo))
    print(r.status_code)
    print(len(r.json()))

    last_commit  = r.json()[0].get('sha')

    r = requests.get('https://api.github.com/repos/{}/{}/commits/{}'.format(user,repo,last_commit))
    root = r.json().get('commit').get('tree').get('sha')

    print_filetree(user, repo, root)
    

def main():
    getFiletreeOfLastCommit('https://github.com/tk-it/web')

if __name__=='__main__':
    main()
