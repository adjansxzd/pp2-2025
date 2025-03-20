import math
import time

def delay(num, mili):
    time.sleep(mili / 1000) # Делает пауза до запуска
    result = math.sqrt(num)
    print(f"Square root of {num} after {mili} miliseconds is {result}")

num, mili = int(input()), int(input())
delay(num, mili)