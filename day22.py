#!/bin/env/python

from collections import deque
from itertools import islice

def parse_input():
    f = open('day22_input.txt', 'r')
    lines = [line.strip() for line in f.readlines()]
    player1, player2 = deque(), deque()
    for line in lines:
        if 'Player 1' in line:
            deck = player1
        elif 'Player 2' in line:
            deck = player2
        elif not line:
            pass
        else:
            deck.append(int(line))
    return player1, player2

def regular_combat(player1, player2):
    while player1 and player2:
        card1, card2 = player1.popleft(), player2.popleft()
        if card1 > card2:
            player1.append(card1)
            player1.append(card2)
        else:
            player2.append(card2)
            player2.append(card1)
    return 1 if player1 else player2

def recursive_combat(player1, player2):
    player1_past_decks, player2_past_decks = set(), set()

    while player1 and player2:
        card1, card2 = player1.popleft(), player2.popleft()

        if len(player1) >= card1 and len(player2) >= card2:
            round_winner = recursive_combat(
                deque(islice(player1, 0, card1)),
                deque(islice(player2, 0, card2)),
            )
        else:
            round_winner = 1 if card1 > card2 else 2

        if round_winner == 1:
            player1.append(card1)
            player1.append(card2)
        else:
            player2.append(card2)
            player2.append(card1)

        if (
            tuple(player1) in player1_past_decks
            or tuple(player1) in player2_past_decks
        ):
            return 1
        player1_past_decks.add(tuple(player1))
        player2_past_decks.add(tuple(player2))

    return 1 if player1 else player2

def play_combat(recursive=False):
    player1, player2 = parse_input()
    if not recursive:
        who_won = regular_combat(player1, player2)
    else:
        who_won = recursive_combat(player1, player2)
    winner = player1 if who_won == 1 else player2
    return sum([card*(len(winner)-i) for i, card in enumerate(winner)])

print(play_combat())
print(play_combat(recursive=True))
