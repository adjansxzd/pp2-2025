import re

pattern = re.compile(r"^a.*b$")
test_strings = ["acb", "Afaow8hB", "a123b", "ab", "aXYZb", "a", "b", "ba"]
matches = [s for s in test_strings if pattern.fullmatch(s)]
print(matches)