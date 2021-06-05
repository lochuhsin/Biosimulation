from os.path import isfile, isdir, join
import os

def files_under_directory(path ='Save/' ,show = False):
        files= os.listdir(path)
        file_container = []
        
        for f in files:
            fullpath = join(path, f)   
            if isfile(fullpath):
                temp = f
                file_container.append(temp)
            elif isdir(fullpath):
                print("directory : ",f)
        
        if show == True:
            print(file_container)            
        return file_container