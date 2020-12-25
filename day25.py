#!/bin/env/python

def parse_input():
    f = open('day25_input.txt', 'r')
    return [int(line.strip()) for line in f.readlines()]

def calculate_loop_size(key):
    value = 1
    subject_num = 7
    loop_size = 0
    while value != key:
        value *= subject_num
        value = value % 20201227
        loop_size += 1
    return loop_size

def transform(subject_num, loop_size):
    value = 1
    for i in range(loop_size):
        value *= subject_num
        value = value % 20201227
    return value

card_pub_key, door_pub_key = parse_input()

card_loop_size = calculate_loop_size(card_pub_key)
print(transform(door_pub_key, card_loop_size))
