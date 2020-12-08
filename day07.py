#!/bin/env/python

import re

f = open('day07_input.txt', 'r')
lines = [line.strip() for line in f.readlines()]

class Bag(object):
    def __init__(self, name):
        self.name = name
        self.inner_bags = set()
        self.outer_bags = set()
        self.inner_bag_count = {}

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

bag_map = {}

def add_rule(bag_map, inner_bag, outer_bag):
    if inner_bag in bag_map:
        bag_map[inner_bag].add(outer_bag)
    else:
        bag_map[inner_bag] = {outer_bag}

    if outer_bag in bag_map:
        for outer_outer_bag in bag_map[outer_bag]:
            add_rule(bag_map, inner_bag, outer_outer_bag)

for line in lines:
    regex = re.match('^(.*) bags contain (.*)\.$', line)
    outer_bag = regex.group(1).strip()
    if outer_bag not in bag_map:
        bag_map[outer_bag] = Bag(outer_bag)
    ob = bag_map[outer_bag]

    inner_bags = [
        inner_bag.strip()
        for inner_bag in regex.group(2).strip().split(',')
    ]
    if inner_bags[0] == 'no other bags':
        bag_map[inner_bags[0]] = Bag(inner_bags[0])
    else:
        for inner_bag in inner_bags:
            regex = re.match('^(\d+) (.*) bags*$', inner_bag)
            count = regex.group(1)
            inner_bag_formatted = regex.group(2)
            if inner_bag_formatted not in bag_map:
                bag_map[inner_bag_formatted] = Bag(inner_bag_formatted)
            ib = bag_map[inner_bag_formatted]
            ob.inner_bags.add(ib)
            ib.outer_bags.add(ob)
            ob.inner_bag_count[ib] = int(count)

def get_outer_bags(bag):
    if bag.outer_bags:
        names = set([ob.name for ob in list(bag.outer_bags)])
        for outer_bag in list(bag.outer_bags):
            names = names.union(get_outer_bags(outer_bag))
        return names
    else:
        return {bag.name}

unique_bag_names = get_outer_bags(bag_map['shiny gold'])
print(len(list(unique_bag_names)))

def get_inner_bag_count(bag):
    if not bag.inner_bag_count:
        return 1

    count = 0
    for ib in bag.inner_bag_count:
        if ib.inner_bag_count:
            count += bag.inner_bag_count[ib]
        count += bag.inner_bag_count[ib] * get_inner_bag_count(ib)
    return count

print(get_inner_bag_count(bag_map['shiny gold']))
