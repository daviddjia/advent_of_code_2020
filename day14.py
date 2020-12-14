#!/bin/env/python

import re
import math

f = open('day14_input.txt', 'r')
lines = [line.strip() for line in f.readlines()]

memory = {}
for line in lines:
    if line[0:4] == 'mask':
        mask = line.split()[2]
        zero_mask = int(mask.replace('X', '1'), 2)
        one_mask = int(mask.replace('X', '0'), 2)
    else:
        regex = re.match('mem\[(\d+)\]\s+=\s+(\d+)', line)
        address, value = int(regex.group(1)), int(regex.group(2))
        value = (value & zero_mask) | one_mask
        memory[address] = value
print(sum(memory.values()))

memory = {}
for line in lines:
    if line[0:4] == 'mask':
        masks = []
        mask = line.split()[2]
        x_indices = []
        for i, char in enumerate(mask):
            if char == 'X':
                x_indices.append(i)
        for i in range(int(math.pow(2, len(x_indices)))):
            bin_num = bin(i)[2:]
            if len(bin_num) != len(x_indices):
                bin_num = bin_num.rjust(len(x_indices), '0')
            zero_mask_list, one_mask_list = list(mask.replace('0', '1')), list(mask)
            one_mask_list = list(mask)
            for j, index in enumerate(x_indices):
                zero_mask_list[index] = one_mask_list[index] = bin_num[j]
            zero_mask, one_mask = ''.join(zero_mask_list), ''.join(one_mask_list)
            masks.append((int(zero_mask, 2), int(one_mask, 2)))
    else:
        regex = re.match('mem\[(\d+)\]\s+=\s+(\d+)', line)
        address, value = int(regex.group(1)), int(regex.group(2))
        for zero_mask, one_mask in masks:
            memory[(address & zero_mask) | one_mask] = value
print(sum(memory.values()))

