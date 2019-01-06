import functools
import argparse
from github import Github
import github
import time
import os

def wait_for_rate_limit(g):
    print(g.rate_limiting_resettime)
    print(time.time())
    while g.rate_limiting_resettime+3600 > time.time() :
        print('Time limit exceeded, seconds remaining: %r' % (g.rate_limiting_resettime+3600-time.time()))
        time.sleep(10)


@functools.lru_cache()
def getFiletreeForRepo(user, repo, g):
    while True:
        try:
            with open('github_info_results/%s-%s.txt'%(user, repo), 'w') as f:
                f.write('#repo:%s/%s \n' % (user, repo))
                print('Visiting:%s/%s \n' % (user, repo)) 
                filetree = {}
                repository = g.get_repo('{}/{}'.format(user, repo))
                contents = repository.get_contents('')
        
                while len(contents) > 1:
                    file_content = contents.pop(0)
                    if file_content.type == 'dir':
                        contents.extend(repository.get_contents(file_content.path))
                    else:
                        path = file_content.path
                        print(path)
                        f.write(path+'\n')
                return
        except github.GithubException as exc:
            print(exc)
            if isinstance(exc, github.RateLimitExceededException):
                wait_for_rate_limit(g)
            else:
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

    result_path = r'./github_info_results'
    if not os.path.exists(result_path):
        os.makedirs(result_path)

    visited_lines = 0
    for line in lines:
        url = line.split('/')
        user, repo = url[3:5]
        try:
            getFiletreeForRepo(user, repo, g)
            visited_lines += 1
        except github.GithubException as exc:
            uf = open(args.file_path, 'w')
            for line in lines[visited_lines:]:
                uf.write(line)


if __name__=='__main__':
    main()
