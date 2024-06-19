#!/usr/bin/env python3

import json
import argparse

class JSONExplorer:
    def __init__(self, style, icon_family):
        self.style = style
        self.icon_family = icon_family

    def render(self, json_data):
        return self.style.render(json_data, self.icon_family)

class Style:
    def render(self, json_data, icons):
        raise NotImplementedError

class TreeStyle(Style):
    def render(self, json_data, icons):
        return self._render_node(json_data, 0, icons)

    def _render_node(self, node, level, icons):
        result = ""
        indent = "│  " * level
        for key, value in node.items():
            if isinstance(value, dict):
                result += f"{indent}├─{icons.getNodeIcon()}{key}\n"
                result += self._render_node(value, level + 1, icons)
            else:
                result += f"{indent}└─{icons.getLeafIcon()}{key}: {value}\n"
        return result

class RectStyle(Style):
    def render(self, json_data, icons):
        result = "┌" + "─" * 66 + "┐\n"  # 添加矩形的上边界
        result += self._render_node(json_data, 0, icons)
        result += "└" + "─" * 66 + "┘\n"  # 添加矩形的下边界
        return result

    def _render_node(self, node, level, icons):
        result = ""
        indent = "│  " * level
        max_length = 60  # 设定每行的最大长度

        for key, value in node.items():
            if isinstance(value, dict):
                line = f"{indent}├─{icons.getNodeIcon()}{key}─" + "─" * (max_length - len(key) - level * 3 - 1) + "┐\n"
                result += line
                result += self._render_node(value, level + 1, icons)
            else:
                line = f"{indent}└─{icons.getLeafIcon()}{key}: {value}─" + "─" * (max_length - len(key) - len(str(value)) - level * 3 - 1) + "┤\n"
                result += line
        return result



class IconFamily:
    def getNodeIcon(self):
        raise NotImplementedError

    def getLeafIcon(self):
        raise NotImplementedError

class PokerIcons(IconFamily):
    def getNodeIcon(self):
        return "♢    "

    def getLeafIcon(self):
        return "♤ "

class OtherIcons(IconFamily):
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
    style = get_style(args.style)
    icon_family = get_icon_family(args.icon)

    explorer = JSONExplorer(style, icon_family)
    print(explorer.render(json_data))

if __name__ == "__main__":
    main()
