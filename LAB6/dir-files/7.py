from shutil import copyfile # shutil - built-in function. С его помощью можно копировать, перемещать, переименовывать и удалять файлы и папки.

try:
    copyfile('test.py', 'abc.py')
    print("File copied.")
except Exception as error:
    print(f"An error: {error}")