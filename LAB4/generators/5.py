def fun(n):
    for i in range(n, -1, -1):
        yield i

n = int(input("n: "))
for i in fun(n):
    print(i)