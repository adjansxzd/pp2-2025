import os

path = open(r"C:\Users\Adilzhan\Documents\pp2\LAB6\dir-files\5ex.txt", "a")
mylist = ["bmw ", "m8 ", "m4 ", "pls."]
for word in mylist:
    path.write(word)