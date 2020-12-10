#!/bin/env/python

f = open('day10_input.txt', 'r')

ratings = [int(line.strip()) for line in f.readlines()]

ratings.extend([0, max(ratings)+3])
ratings.sort()

prev = 0
diff_map = {}
for rating in ratings[1:]:
    diff = rating-prev
    diff_map[diff] = diff_map.get(diff, 0) + 1
    prev = rating
print(diff_map[1]*diff_map[3])

num_paths = {}
for i, rating in enumerate(ratings):
    num_path = 0
    for diff in [1, 2, 3]:
        if i-diff >= 0 and rating-ratings[i-diff] <= 3:
            num_path += num_paths[i-diff]
    num_paths[i] = max(num_path, 1)
print(num_path)
