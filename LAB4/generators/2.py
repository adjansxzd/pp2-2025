def fun(num):
    for i in range(num):
        if(i % 2 == 0):
            yield i

num = int(input())
mylist = list(fun(num))
print(mylist)
