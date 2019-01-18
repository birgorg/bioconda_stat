import functools
import argparse
from github import Github
import github
import time
import os
from collections import Counter

def wait_for_rate_limit(g):
    resettime = g.rate_limiting_resettime
    while resettime > time.time() :
        print('Time limit exceeded, seconds remaining: %r' % (resettime-time.time()))
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


def mineRepos(file_path, token):
    f = open(file_path, 'r')
    lines = f.readlines()
    f.close()
    
    if token != None:
        g = Github(token)
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


def countFileExtensions(files_path):
    python_setup = 0
    makefile_in_root = 0
    extension_counter = Counter()
    files = os.listdir(files_path)
    for file_name in files:
        extension_set = set()
        with open('%s%s' % (files_path, file_name), 'r') as f:
            for line in f.readlines():
                line.strip('\n')
                line.lower()
                extension = line.split('.')[-1:]
                if not extension[0] == line:
                    extension_set.add(extension[0])
                if 'setup.py' == line:
                    python_setup += 1
                    print(line)
                elif 'makefile' == line:
                    makefile_in_root += 1
                    print(line)
        for ext in extension_set:
            extension_counter[ext] += 1
    print('Number of repos with setup.py: %r' % python_setup)
    print('Number of makefiles in root of repos: %r' % makefile_in_root)
    print('10 most common extensions: ' + str(extension_counter.most_common(10)))

def main():
    parser = argparse.ArgumentParser(description="Script for counting files in github repo")
    parser.add_argument('-c', '--count', action='store_true', help='If this flag i set, the script will tage the directory given in file_path, run through all the .txt files and count file extensions')
    parser.add_argument('file_path', help="path to file containing repo urls, one url for each line")
    parser.add_argument('-t', '--token', help='Github token for getting a better rate limit', default=None)
    args = parser.parse_args()

    if(args.count):
        countFileExtensions(args.file_path)
    else:
        mineRepos(args.file_path, args.token)

if __name__=='__main__':
    main()
