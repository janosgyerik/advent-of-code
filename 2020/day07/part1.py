#!/usr/bin/env python3
import json
import sys
from collections import Counter, defaultdict


def parse(lines):
    rules = {}
    for line in lines:
        container, rest = line.split(' bags contain ')
        rules[container] = ruleset = {}
        if rest.startswith('no other'):
            continue

        for bag in rest.split(', '):
            count, color1, color2, _ = bag.split(' ')
            count = int(count)
            color = color1 + ' ' + color2
            ruleset[color] = count

    return rules


def build_rgraph(rules):
    g = defaultdict(set)
    for container, contents in rules.items():
        for color, _ in contents.items():
            g[color].add(container)

    return g


def find_unique_nodes(tree, root):
    unique_nodes = set()

    def dfs(node):
        unique_nodes.add(node)
        for child in tree[node]:
            dfs(child)

    dfs(root)
    return unique_nodes


def count_bags(rules, color):
    return 1 + sum(count * count_bags(rules, color2) for color2, count in rules[color].items())


def main():
    lines = [line.strip() for line in sys.stdin.readlines()]
    rules = parse(lines)
    # print(json.dumps(rules, indent=2))
    rgraph = build_rgraph(rules)
    # print(rgraph)
    leafs = find_unique_nodes(rgraph, 'shiny gold')
    print(len(leafs) - 1)

    print(count_bags(rules, 'shiny gold') - 1)


if __name__ == '__main__':
    main()
