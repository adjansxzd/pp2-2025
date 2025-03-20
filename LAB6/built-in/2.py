text = str(input())
upper_cnt, lower_cnt = 0, 0
for char in text:
    if(char.islower()):
        lower_cnt += 1
    else:
        upper_cnt += 1

print("Upper case:", upper_cnt)
print("Lower case:", lower_cnt)