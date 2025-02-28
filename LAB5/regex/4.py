import re

pattern = re.compile(r"[A-Z]{1}[a-z]+")
text = ("London is the Capital of Great Britaniyaaa")
matches = pattern.findall(text)
print(matches)
