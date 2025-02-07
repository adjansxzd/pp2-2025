# x + y = numheads
# 2x + 4y = numlegs
# 2 * (numheads - y) + 4 * y = numlegs
# 2numheads + 2y = numlegs
# 2y = numlegs - 2numheads
# y = (numlegs - 2numheads) / 2

def solve(numheads, numlegs):
    y = (numlegs - 2 * numheads) // 2
    x = numheads - y
    if 2 * x + 4 * y == numlegs:
        return x, y
    
numheads = 35
numlegs = 94
print(solve(numheads, numlegs))    

