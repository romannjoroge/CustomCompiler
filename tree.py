from typing import Dict, List, Tuple
from collections import defaultdict
from dsplot.graph import Graph
# a tree-like data structure
class Tree:

    TAB = "   "
    def __init__(self):
        self.data     = ""
        self.children = []

    def add(self, child):
        self.children.append(child)

    def print(self, tab = ""):
        if self.data != "":
            print(tab + self.data)
            tab += self.TAB
            for child in self.children:
                if isinstance(child, Tree):
                    child.print(tab)
                else:
                    print(tab + child)

class MyTree:
    def __init__(self):
        self.data = defaultdict(list)
        self.display_data = defaultdict(list)

    def add(self, parent: Tuple[str, int], item: Tuple[str, int]):
        if parent == None:
            self.data[item] = []
        else:
            self.data[parent].append(item)

            if self.data[item] == None:
                self.data[item] = []

    def add_display(self, parent: int, item: int):
        print(f"Parent {parent} and its child {item} are being added to display tree")
        if parent is None:
            self.display_data[item] = []
        else:
            self.display_data[parent].append(item)

            if self.display_data[item] == None:
                self.display_data[item] = []

        print("Display Data items => ", self.display_data)

    def display(self):
        g = Graph(self.display_data)
        g.plot()
