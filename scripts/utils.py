import os
import fileinput

def filepath_normalizer(path_to_folder):
    _, _, files = next(os.walk(path_to_folder))
    for f in files:
        for line in fileinput.input(path_to_folder + "/" + f, inplace=True):
            line = line.lower()
            if line.startswith("/"):
                line = line[1:]
            print(line)
            
        
            
                    
                         


