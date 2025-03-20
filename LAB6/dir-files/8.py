import os

path = (r"C:\Users\Adilzhan\Documents\pp2\LAB6\dir-files\deletefile.txt")
if os.path.exists(path):    
    os.remove(path)
else:
    print("This file doesn't exist.")