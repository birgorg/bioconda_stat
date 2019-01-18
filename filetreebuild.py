import os

def build_filetree(startpath, name):
    with open('results/%s.txt' % name, 'w') as f:
        f.write('#package: %s \n' % name)
        for root, dirs, files in os.walk(startpath):
            newroot = root.replace(startpath, '')
            for fp in files:
               f.write(newroot+fp) 

if __name__ == '__main__':
    build_filetree('/home/fuan/Documents')
