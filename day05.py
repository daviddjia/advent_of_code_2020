#!/bin/env/python

f = open('day05_input.txt', 'r')

lines = [line.strip() for line in f.readlines()]

seat_ids = []
for line in lines:
    row_code = line[0:7]
    col_code = line[7:]
    row = 0
    col = 0

    for i, char in enumerate(row_code[::-1]):
        if char == 'B':
            row += 1 << i
    for i, char in enumerate(col_code[::-1]):
        if char == 'R':
            col += 1 << i

    seat_id = row*8+col
    seat_ids.append(seat_id)
print(max(seat_ids))

sorted_seat_ids = sorted(seat_ids)
for i, seat_id in enumerate(sorted_seat_ids[1:]):
    if seat_id-1 != sorted_seat_ids[i]:
        print(str(seat_id-1))
