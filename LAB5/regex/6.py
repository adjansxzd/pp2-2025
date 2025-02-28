import re

test = """The morning had dawned clear and cold, with a crispness that hinted at the end of 
summer. They set forth at daybreak to see a man beheaded, twenty in all, and Bran rode 
among them, nervous with excitement."""
pattern = re.sub(r"[ .,]", ":", test)
print(pattern)
