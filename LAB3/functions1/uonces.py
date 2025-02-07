def converter(grams):
    return 28.3495231 * grams

grams = float(input("Enter the number of grams: "))
ounces = converter(grams)
print(ounces)