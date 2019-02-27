import requests
import zipfile
import shutil
import os
import tarfile
from distutils.dir_util import copy_tree

def download_package(url_to_package):
    if not url_to_package.startswith("http"):
        return ""
    try:
        r = requests.get(url_to_package, stream=True)
    except:
        return ""

    if url_to_package.endswith(".tar.gz"):
        temp_file_path = "temp.tar.gz"
    elif url_to_package.endswith(".zip"):
        temp_file_path = "temp.zip"
    else:
        return ""

    with open(temp_file_path, "wb") as code:
        code.write(r.content)
    
    return temp_file_path

def unpack_package(temp_file_path):
    try:
        if temp_file_path == "temp.tar.gz":
            tf = tarfile.open(temp_file_path)
            tf.extractall('tmp')
            tf.close()
        else:
            zip_ref = zipfile.ZipFile(temp_file_path, 'r')
            zip_ref.extractall('tmp')
            zip_ref.close()
    except:
        os.mkdir('tmp')
        pass

def build_filetree(startpath, name, url):
    with open('../results/%s.txt' % name, 'w') as f:    
        f.write('#package: %s \n' % name)
        f.write('#url: %s \n' % url)
        for root, dirs, files in os.walk(startpath):
            newroot = root.replace(startpath, '')
            for fp in files:
               f.write(newroot + "/" + fp + "\n")


def clean(temp_file_path, name):
    # copy package into bioconda_packages
    try:
        copy_tree("tmp", "../bioconda_packages/")
    except:
        print("Error: Couldn't copy %s into the packages folder" % name)

    # remove the unpacked temp files 
    shutil.rmtree('tmp')
    
    # remove the downloaded .zip, .tar.gz or .tar file
    os.remove(temp_file_path)


# downloads all bioconda packages from the urls in all_urls.txt in the urls folder
def download_all_packages():
    with open("../urls/all_urls.txt", "r") as f:
        for url in f.readlines():
            print("Next url to handle: %s" % url)
            temp_file_path = download_package(url.strip("\n"))
            if temp_file_path != "":  
                unpack_package(temp_file_path)
                name = ''
                path = 'tmp'
                root, dirs, files = next(os.walk(path))
                while len(dirs) == 1 and len(files) == 0:
                    path += '/'+dirs[0]
                    name = dirs[0]
                    root, dirs, files = next(os.walk(path))
                build_filetree(path, name, url)
                clean(temp_file_path, name)
    

if __name__ == "__main__":
    download_all_packages()

    
    
