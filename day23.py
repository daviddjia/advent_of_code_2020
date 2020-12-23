#!/bin/env/python

from collections import deque

def parse_input():
    return deque([
        int(char) for char in open('day23_input.txt', 'r').readline()
        if char != '\n'
    ])

# Only works for part 1
def naive_cup_simulation(cups):
    for move in range(100):
        curr_cup = cups.popleft()
        triplet = [cups.popleft() for _ in range(3)]
        if min(cups) < curr_cup:
            dest_cup = max([c for c in cups if c < curr_cup])
        else:
            dest_cup = max(cups)
        dest_cup_index = cups.index(dest_cup)
        for c in reversed(triplet):
            cups.insert(dest_cup_index+1, c)
        cups.append(curr_cup)

    while cups[0] != 1:
        cups.append(cups.popleft())
    return ''.join([str(c) for c in cups if c!=1])

class Node(object):
    def __init__(self, val, prev, next):
        self.val = val
        self.prev = prev
        self.next = next

    def __repr__(self):
        return str(self.val)

    def __str__(self):
        return str(self.val)

class CLL(object):
    def __init__(self):
        self.head = None
        self.node_map = {}

    def append(self, val):
        if not self.head:
            self.head = Node(val, None, None)
            self.head.prev = self.head
            self.head.next = self.head
            self.node_map[val] = self.head
        else:
            tail = self.head.prev
            node = Node(val, tail, self.head)
            tail.next = node
            self.head.prev = node
            self.node_map[val] = node

    def popleft(self):
        val = self.head.val
        old_head = self.head
        tail = self.head.prev
        self.head = self.head.next
        self.head.prev = tail
        tail.next = self.head
        del old_head
        del self.node_map[val]
        return val

    def append_behind(self, val, existing_val):
        existing_node = self.node_map[existing_val]
        next_existing_node = existing_node.next
        node = Node(val, existing_node, next_existing_node)
        existing_node.next = node
        next_existing_node.prev = node
        self.node_map[val] = node

    def print(self):
        l = [self.head.val]
        temp = self.head.next
        while temp.val != self.head.val:
            l.append(temp.val)
            temp = temp.next
        print(l)

    def get_result1(self):
        node = self.node_map[1].next
        l = []
        while node.val != 1:
            l.append(str(node.val))
            node = node.next
        return ''.join(l)

    def get_result2(self):
        node = self.node_map[1]
        return node.next.val * node.next.next.val

def efficient_cup_simulation(cups, part2=False):
    if not part2:
        moves = 100
        max_num = max(cups)
    else:
        moves = 10000000
        max_num = 1000000

    cll = CLL()
    for c in cups:
        cll.append(c)
    for c in range(max(cups)+1, max_num+1):
        cll.append(c)

    for move in range(moves):
        curr_cup = cll.popleft()
        triplet = [cll.popleft() for _ in range(3)]

        dest_cup = (curr_cup-2)%(max_num)+1
        while dest_cup in triplet:
            dest_cup = (dest_cup-2)%(max_num)+1
        for c in reversed(triplet):
            cll.append_behind(c, dest_cup)
        cll.append(curr_cup)

    if not part2:
        return cll.get_result1()
    else:
        return cll.get_result2()

# print(naive_cup_simulation(parse_input()))
print(efficient_cup_simulation(parse_input()))
print(efficient_cup_simulation(parse_input(), part2=True))
