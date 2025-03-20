import os

def dir_f(path):
    print("Only directories:")
    for name in os.listdir(path):
        if os.path.isdir(os.path.join(path, name)):
            print(name)
    
    print("\nOnly files:")
    for name in os.listdir(path):
        if os.path.isfile(os.path.join(path, name)):
            print(name)
    
    print("\nAll directories and files:")
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            print(os.path.join(root, dir))
        for file in files:
            print(os.path.join(root, file))

path = 'C:\\Users\\Adilzhan\\Documents\\pp2'
dir_f(path)
