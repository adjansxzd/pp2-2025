import re

pattern = re.compile(r"[a-z]+_[a-z]+")
text = ("aaa_bbb hello_world Hello_World tma_bot ya_ya_ya")
matches = pattern.findall(text)
print(matches)