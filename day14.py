#!/bin/env/python

import re
import math

f = open('day14_input.txt', 'r')
lines = [line.strip() for line in f.readlines()]

def parse_memory_instruction(line):
    return tuple(int(i) for i in re.findall('(\d+)', line))

memory = {}
for line in lines:
    if 'mask' in line:
        mask = line.split()[2]
        zero_mask = int(mask.replace('X', '1'), 2)
        one_mask = int(mask.replace('X', '0'), 2)
    else:
        address, value = parse_memory_instruction(line)
        value = (value & zero_mask) | one_mask
        memory[address] = value
print(sum(memory.values()))

memory = {}
for line in lines:
    if 'mask' in line:
        masks = []
        mask = line.split()[2]
        x_indices = [i for i, char in enumerate(mask) if char == 'X']
        for i in range(int(math.pow(2, len(x_indices)))):
            bin_num = bin(i)[2:].zfill(len(x_indices))
            zero_mask_list, one_mask_list = list(mask.replace('0', '1')), list(mask)
            for j, index in enumerate(x_indices):
                zero_mask_list[index] = one_mask_list[index] = bin_num[j]
            zero_mask, one_mask = ''.join(zero_mask_list), ''.join(one_mask_list)
            masks.append((int(zero_mask, 2), int(one_mask, 2)))
    else:
        address, value = parse_memory_instruction(line)
        for zero_mask, one_mask in masks:
            memory[(address & zero_mask) | one_mask] = value
print(sum(memory.values()))
