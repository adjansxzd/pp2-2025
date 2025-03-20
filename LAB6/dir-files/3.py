import os

path = r'C:\Users\Adilzhan\Documents\pp2'
if(os.path.exists(path)):
    print("Such path exists. ")
    filename = os.path.basename(path)
    directory = os.path.dirname(path)
    print("Filename: ", filename)
    print("Directory: ", directory)
else:
    print("Such path doesn't exist")