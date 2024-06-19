#!/usr/bin/env python3

import json
import argparse
from collections.abc import Iterator, Iterable

class JSONIterator(Iterator):
    def __init__(self, json_data):
        self.stack = [(None, json_data)]
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if not self.stack:
            raise StopIteration
        key, value = self.stack.pop()
        if isinstance(value, dict):
            for k, v in reversed(value.items()):
                self.stack.append((k, v))
        return key, value

class JSONExplorer:
    def __init__(self, style_strategy, icon_strategy):
        self.style_strategy = style_strategy
        self.icon_strategy = icon_strategy

    def render(self, json_data):
        iterator = JSONIterator(json_data)
        return self.style_strategy.render(iterator, self.icon_strategy)

class StyleStrategy:
    def render(self, iterator, icon_strategy):
        raise NotImplementedError

class TreeStyle(StyleStrategy):
    def render(self, iterator, icon_strategy):
        result = ""
        level = -1
        indent_stack = []

        for key, value in iterator:
            if key is None:
                continue
            while indent_stack and indent_stack[-1] != key:
                indent_stack.pop()
                level -= 1

            level += 1
            indent_stack.append(key)
            indent = "│  " * level

            if isinstance(value, dict):
                result += f"{indent}├─{icon_strategy.getNodeIcon()}{key}\n"
            else:
                result += f"{indent}└─{icon_strategy.getLeafIcon()}{key}: {value}\n"

        return result

class RectStyle(StyleStrategy):
    def render(self, iterator, icon_strategy):
        result = "┌" + "─" * 66 + "┐\n"
        level = -1
        indent_stack = []
        max_length = 60

        for key, value in iterator:
            if key is None:
                continue
            while indent_stack and indent_stack[-1] != key:
                indent_stack.pop()
                level -= 1

            level += 1
            indent_stack.append(key)
            indent = "│  " * level

            if isinstance(value, dict):
                line = f"{indent}├─{icon_strategy.getNodeIcon()}{key}─" + "─" * (max_length - len(key) - level * 3 - 1) + "┐\n"
                result += line
            else:
                line = f"{indent}└─{icon_strategy.getLeafIcon()}{key}: {value}─" + "─" * (max_length - len(key) - len(str(value)) - level * 3 - 1) + "┤\n"
                result += line

        result += "└" + "─" * 66 + "┘\n"
        return result

class IconStrategy:
    def getNodeIcon(self):
        raise NotImplementedError

    def getLeafIcon(self):
        raise NotImplementedError

class PokerIcons(IconStrategy):
    def getNodeIcon(self):
        return "♢    "

    def getLeafIcon(self):
        return "♤ "

class OtherIcons(IconStrategy):
    def getNodeIcon(self):
        return "★   "

    def getLeafIcon(self):
        return "☆ "

def parse_arguments():
    parser = argparse.ArgumentParser(description='Funny JSON Explorer')
    parser.add_argument('-f', '--file', type=str, required=True, help='Path to the JSON file')
    parser.add_argument('-s', '--style', type=str, required=True, choices=['tree', 'rect'], help='Visualization style (tree or rect)')
    parser.add_argument('-i', '--icon', type=str, required=True, choices=['poker', 'default'], help='Icon family (poker or other)')
    return parser.parse_args()

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def get_style(style_name):
    if style_name == 'tree':
        return TreeStyle()
    elif style_name == 'rect':
        return RectStyle()
    else:
        raise ValueError(f"Unknown style: {style_name}")

def get_icon_family(icon_name):
    if icon_name == 'poker':
        return PokerIcons()
    elif icon_name == 'default':
        return OtherIcons()
    else:
        raise ValueError(f"Unknown icon family: {icon_name}")

# 主程序
def main():
    args = parse_arguments()
    json_data = load_json(args.file)
    style_strategy = get_style(args.style)
    icon_strategy = get_icon_family(args.icon)

    explorer = JSONExplorer(style_strategy, icon_strategy)
    print(explorer.render(json_data))

if __name__ == "__main__":
    main()
