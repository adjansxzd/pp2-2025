import os

path = r'C:\Users\Adilzhan\Documents\pp2\dir-files'
print("Exist:", os.path.exists(path))
print("Readable:", os.access(path, os.R_OK))
print("Writable:", os.access(path, os.W_OK))
print("Executable:", os.access(path, os.X_OK))