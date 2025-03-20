import string, os

if not os.path.exists("Letters"):
    os.makedirs("Letters")
for letter in string.ascii_uppercase:
    with open(f"Letters/{letter}.txt", "w") as f:
        f.writelines(letter)