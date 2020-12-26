#!/bin/env/python

import re

def parse_file():
    f = open('day19_input.txt', 'r')
    # f = open('temp.txt', 'r')
    lines = [line.strip() for line in f.readlines()]

    rules, messages = {}, []
    for i, line in enumerate(lines):
        if not line:
            break
        rule_num, rule_str = line.split(':')
        rule_num = int(rule_num)
        if '"' in rule_str:
            rules[rule_num] = rule_str[-2]
        else:
            rules[rule_num] = [
                [int(num) for num in nums.strip().split(' ')]
                for nums in rule_str.split('|')
            ]
    messages = lines[i+1:]
    return rules, messages

def get_match_strings(rules, rule_num):
    if rules[rule_num] in ('a', 'b'):
        return [rules[rule_num]]
    match_strings = []
    for rule_group in rules[rule_num]:
        rule_group_results = []
        for i, child_rule_num in enumerate(rule_group):
            rule_group_results.append(tuple(get_match_strings(
                rules,
                child_rule_num,
            )))
        match_strings.extend([
            ''.join(result)
            for result in product(*rule_group_results)
        ])
    return match_strings

def part1_solution():
    rules, messages = parse_file()
    match_strings = set(get_match_strings(rules, 0))
    match_count = 0
    for message in messages:
        if message in match_strings:
            match_count += 1
    return match_count

def get_match_regexes(rules, rule_num, depth=0, max_depth=0):
    if rules[rule_num] in ('a', 'b'):
        return rules[rule_num]

    if rule_num in (8, 11):
        if depth <= max_depth:
            depth += 1
        else:
            return ''

    match_regexes = []
    for rule_group in rules[rule_num]:
        rule_group_regex = ''.join([
            get_match_regexes(
                rules,
                child_rule_num,
                depth=depth,
                max_depth=max_depth,
            )
            for child_rule_num in rule_group
        ])
        match_regexes.append(f'{rule_group_regex}')
    match_regexes_str = '|'.join(match_regexes)
    return f'({match_regexes_str})'

def general_solution(part1=False):
    rules, messages = parse_file()
    if not part1:
        rules[8] = [[42], [42, 8]]
        rules[11] = [[42, 31], [42, 11, 31]]
        match_regex = get_match_regexes(
            rules,
            0,
            depth=0,
            max_depth=max(len(m) for m in messages)-min(len(m) for m in messages),
        )
    else:
        match_regex = get_match_regexes(rules, 0)
    match_count = 0
    for message in messages:
        if re.match(f'^{match_regex}$', message):
            match_count += 1
    return match_count

# print(part1_solution())
print(general_solution(part1=True))
print(general_solution())
