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

    def add(self, parent: Tuple[str, int], item: Tuple[str, int]):
        if parent == None:
            print("Item => ", item)
            identifier = item[0] + str(item[1])
            self.data[item[1]] = []
        else:
            print("Parent => ", parent, parent[0], parent[1])
            identifier = parent[0] + " " + str(parent[1])
            itemStore = item[0] + " " + str(item[1])
            print("Identifier => ", identifier, "Itestore => ", itemStore)
            self.data[parent[1]].append(item[1])

            if self.data[item[1]] == None:
                self.data[item[1]] = []

    def display(self):
        g = Graph(self.data)
        g.plot()
