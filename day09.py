#!/bin/env/python

from collections import deque
from itertools import combinations

f = open('day09_input.txt', 'r')
nums = [int(line.strip()) for line in f.readlines()]

preamble = deque(nums[:25])
for num in nums[25:]:
    found_sum = False
    for (x, y) in combinations(preamble, 2):
        if x == y:
            break
        if x+y == num:
            found_sum = True
            break

    if not found_sum:
        break

    preamble.popleft()
    preamble.append(num)
print(num)

result = num
for i, num in enumerate(nums):
    sum = num
    for j, x in enumerate(nums[i+1:]):
        sum += x
        if sum == result:
            print(min(nums[i:i+j+2]) + max(nums[i:i+j+2]))
        elif sum > result:
            break
