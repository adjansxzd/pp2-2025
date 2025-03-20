n = int(input())
pr = 1
total = 0
for i in range(1, n + 1):
    pr *= i
    total += pr
print(total)    