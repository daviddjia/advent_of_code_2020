#!/bin/env/python

from functools import reduce

f = open('day16_input.txt', 'r')
# f = open('test.txt', 'r')
lines = [line.strip() for line in f.readlines()]

newline_index1, newline_index2 = tuple(
    i for i, line in enumerate(lines)
    if line == '')
rules = {}
for line in lines[0:newline_index1]:
    rule, ranges_str = line.split(':')
    range1_str, _, range2_str = ranges_str.split()
    rules[rule] = [
        tuple([int(num) for num in range1_str.split('-')]),
        tuple([int(num) for num in range2_str.split('-')])]
my_ticket = [int(field) for field in lines[newline_index2-1].split(',')]
other_tickets = [
    [int(field) for field in line.split(',')]
    for line in lines[newline_index2+2:]]

error_rate = 0
invalid_ticket_indexes = set()
for i, ticket in enumerate(other_tickets):
    for field in ticket:
        in_range = False
        for ranges in rules.values():
            for lower, upper in ranges:
                if lower <= field <= upper:
                    in_range = True
                    break
            if in_range:
                break
        if not in_range:
            error_rate += field
            invalid_ticket_indexes.add(i)
print(error_rate)

other_valid_tickets = [
    ticket for i, ticket in enumerate(other_tickets)
    if i not in invalid_ticket_indexes]
def _get_summed_ranges(ranges):
    range1, range2 = ranges
    return (range1[1]-range1[0]) + (range2[1]-range2[0])
sorted_rules = sorted(rules, key=lambda rule: _get_summed_ranges(rules[rule]))

rule_index_map = {}
possible_index_rule_map = {}
for index in range(len(my_ticket)):
    possible_index_rule_map[index] = set()
    for rule in rules:
        range1, range2 = rules[rule]
        for ticket in other_valid_tickets:
            field = ticket[index]
            if not (
                range1[0] <= field <= range1[1]
                or range2[0] <= field <= range2[1]
            ):
                break
        else:
            possible_index_rule_map[index].add(rule)

while len(possible_index_rule_map) > 0:
    for index in possible_index_rule_map:
        if len(possible_index_rule_map[index]) == 1:
            rule = possible_index_rule_map[index].pop()
            break
    del possible_index_rule_map[index]
    for index2 in possible_index_rule_map:
        if rule in possible_index_rule_map[index2]:
            possible_index_rule_map[index2].remove(rule)
    rule_index_map[index] = rule

print(reduce(
    lambda x,y:x*y,
    [
        field for i, field in enumerate(my_ticket)
        if 'departure' in rule_index_map[i]
    ]))
