import re

text = "The_Morning_Had_Dawned_Clear_And_Cold"
razdelit = text.split('_') # разделить текст на список из слов: ['The', 'Morning', 'Had', 'Dawned', 'Clear', 'And', 'Cold']

soedinit = razdelit[0] + ''.join(word.lower() for word in razdelit[1:])
print(soedinit)