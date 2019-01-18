import requests
import zipfile
import shutil
import os
import tarfile


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
            #path_to_dir = os.path.commonprefix(tf.getnames()).replace('/','').replace('.','')
            tf.extractall('tmp')
            tf.close()
        else:
            zip_ref = zipfile.ZipFile(temp_file_path, 'r')
            #path_to_dir = zip_ref.namelist()[0].replace('/','').replace('.','')
            #print(zip_ref.filename)
            zip_ref.extractall('tmp')
            zip_ref.close()
    except:
        os.mkdir('tmp')
        #os.mkdir('tmp/fail')
        pass

def build_filetree(startpath, name):
    with open('results/%s.txt' % name, 'w') as f:
        f.write('#package: %s \n' % name)
        for root, dirs, files in os.walk(startpath):
            newroot = root.replace(startpath, '')
            for fp in files:
               f.write(newroot + "/" + fp + "\n")


def clean(temp_file_path):
    shutil.rmtree('tmp')
    os.remove(temp_file_path)

if __name__ == "__main__":
    with open("noneGithubUrls.txt", "r") as f:
        for url in f.readlines():
            print(url)
            temp_file_path = download_package(url.strip("\n"))
            if temp_file_path != "":  
                #path_to_dir = unpack_package(temp_file_path)
                unpack_package(temp_file_path)
                name = ''
                path = 'tmp'
                root, dirs, files = next(os.walk(path))
                while len(dirs) == 1 and len(files) == 0:
                    path += '/'+dirs[0]
                    name = dirs[0]
                    root, dirs, files = next(os.walk(path))
                build_filetree(path, name)
                clean(temp_file_path)
    
    
