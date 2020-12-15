#!/bin/env/python

f = open('day15_input.txt', 'r')
initial_numbers = [int(num) for num in f.readline().split(',')]

def play_game(initial_numbers, n):
    num_map = {num: (-1, i+1) for i, num in enumerate(initial_numbers)}
    prev_num = initial_numbers[-1]
    for i in range(len(initial_numbers)+1, n+1):
        last_last, last = num_map[prev_num]
        if last_last == -1:
            curr_num = 0
        else:
            curr_num = last - last_last
        if curr_num in num_map:
            num_map[curr_num] = (num_map[curr_num][1], i)
        else:
            num_map[curr_num] = (-1, i)
        prev_num = curr_num
    return prev_num

print(play_game(initial_numbers, 2020))
print(play_game(initial_numbers, 30000000))
