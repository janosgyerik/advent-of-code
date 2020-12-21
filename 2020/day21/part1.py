#!/usr/bin/env python

import sys
from collections import defaultdict


def read_lines(path):
    with open(path) as fh:
        return [line.rstrip() for line in fh.readlines()]


class Food:
    def __init__(self, ingredients, allergens):
        self.ingredients = set(ingredients)
        self.allergens = set(allergens)

    def common_ingredients(self, other):
        return self.ingredients.intersection(other.ingredients)

    def common_allergens(self, other):
        return self.allergens.intersection(other.allergens)


def parse_food(line):
    ingredients = line[:line.index('(') - 1].split(' ')
    assert not any(' ' in x for x in ingredients)

    marker = '(contains '
    allergens = line[line.index(marker) + len(marker):-1].split(', ')
    assert not any(' ' in x for x in allergens)

    return Food(ingredients, allergens)


def find_ingredient_allergen(foods, unmapped_allergens):
    for f in foods:
        if len(f.ingredients) == 1 == len(f.allergens):
            return list(f.ingredients)[0], list(f.allergens)[0]

    for allergen in unmapped_allergens:
        ingredients = set()
        for food in foods:
            if allergen in food.allergens:
                ingredients.update(food.ingredients)
                break

        for food in foods:
            if allergen in food.allergens:
                ingredients = ingredients.intersection(food.ingredients)
                if len(ingredients) == 1:
                    return list(ingredients)[0], allergen


def find_safe_ingredients(foods):
    known_allergens = set()
    for food in foods:
        known_allergens.update(food.allergens)

    mapped_allergens = {}
    unmapped_allergens = known_allergens.copy()

    while True:
        pair = find_ingredient_allergen(foods, unmapped_allergens)
        if not pair:
            break

        ingredient, allergen = pair
        mapped_allergens[ingredient] = allergen

        for f in foods:
            if ingredient in f.ingredients:
                f.ingredients.remove(ingredient)
                if allergen in f.allergens:
                    f.allergens.remove(allergen)

    assert len(known_allergens) == len(mapped_allergens)
    assert all(len(f.allergens) == 0 for f in foods)

    print(','.join(sorted(mapped_allergens.keys(), key=lambda k: mapped_allergens[k])))
    return sum(len(f.ingredients) for f in foods)


def main():
    lines = read_lines(sys.argv[1])
    foods = [parse_food(line) for line in lines]
    safe_foods = find_safe_ingredients(foods)
    print(safe_foods)
    # 2338 is too high


if __name__ == '__main__':
    main()
