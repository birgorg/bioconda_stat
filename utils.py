import os
import fileinput

def filepath_normalizer(path_to_folder):
    _, _, files = next(os.walk(path_to_folder))
    for f in files:
        #with open(path_to_folder + "/" + f, "r+") as cur_f:
                #for line in cur_f.readlines():

        for line in fileinput.input(path_to_folder + "/" + f, inplace=True):
            line = line.lower()
            if line.startswith("/"):
                line = line[1:]
            print(line)
            
        
            
                    
                         


