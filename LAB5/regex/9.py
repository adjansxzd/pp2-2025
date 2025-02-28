import re

text = "TheMorningHadDawnedClearAndCold"
pattern = re.findall(r"[A-Z][a-z]*", text)
space = ' '.join(pattern)
print(space)