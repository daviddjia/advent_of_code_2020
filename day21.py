#!/bin/env/python

import re

def parse_input():
    f = open('day21_input.txt', 'r')
    lines = [line.strip() for line in f.readlines()]
    foods = []
    for line in lines:
        regex = re.match('^(.*) \(contains (.*)\)$', line)
        food = regex.group(1).split()
        allergens = [a.strip() for a in regex.group(2).split(',')]
        foods.append((food, allergens))
    return foods

def build_data_structures(foods):
    all_allergens = set()
    for _, allergens in foods:
        for allergen in allergens:
            all_allergens.add(allergen)

    food_map = {allergen: [] for allergen in all_allergens}
    ingredient_map = {allergen: set() for allergen in all_allergens}
    for food, allergens in foods:
        for allergen in allergens:
            food_map[allergen].append(food)
            ingredient_map[allergen].update(set(food))

    return food_map, ingredient_map

def find_safe_ingredients(foods, food_map, ingredient_map):
    safe_ingredient_map = {allergen: [] for allergen in food_map}
    for allergen, ingredients in ingredient_map.items():
        for ingredient in ingredients:
            foods = food_map[allergen]
            if len(foods) == 1:
                continue
            for food in foods:
                if ingredient not in food:
                    safe_ingredient_map[allergen].append(ingredient)
                    break

    safe_ingredients = set()
    for _, ingredients in safe_ingredient_map.items():
        for ingredient in ingredients:
            safe_ingredients.add(ingredient)

    for allergen, ingredients in safe_ingredient_map.items():
        for ingredient in ingredients:
            for other_allergen in ingredient_map:
                if other_allergen == allergen:
                    continue
                if (
                    ingredient in ingredient_map[other_allergen]
                    and ingredient not in safe_ingredient_map[other_allergen]
                ):
                    if ingredient in safe_ingredients:
                        safe_ingredients.remove(ingredient)
    return safe_ingredients

def count_safe_ingredients(foods, safe_ingredients):
    count = 0
    for si in safe_ingredients:
        for food, _ in foods:
            if si in food:
                count += 1
    return count

def identify_allergens(safe_ingredients, food_map, ingredient_map):
    for allergen, ingredients in ingredient_map.items():
        for safe_ingredient in safe_ingredients:
            if safe_ingredient in ingredients:
                ingredients.remove(safe_ingredient)

    possible_matches = {}
    for allergen, foods in food_map.items():
        common_ingredients = set(foods[0])
        for food in foods:
            common_ingredients = common_ingredients.intersection(set(food))
        possible_matches[allergen] = common_ingredients

    matches = {}
    while possible_matches:
        allergen = sorted(
            list(possible_matches),
            key=lambda a: len(possible_matches[a]),
        )[0]
        ingredient = possible_matches[allergen].pop()
        del possible_matches[allergen]
        matches[ingredient] = allergen
        for a in possible_matches:
            if ingredient in possible_matches[a]:
                possible_matches[a].remove(ingredient)

    return ','.join(sorted(matches, key=lambda i:matches[i]))

foods = parse_input()
food_map, ingredient_map = build_data_structures(foods)
safe_ingredients = find_safe_ingredients(foods, food_map, ingredient_map)
print(count_safe_ingredients(foods, safe_ingredients))
print(identify_allergens(safe_ingredients, food_map, ingredient_map))
