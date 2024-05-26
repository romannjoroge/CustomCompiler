from scanner import Scanner
from parser_1 import parse

tokens = Scanner()
tree = parse(tokens, [])
print(f"\n\n----------------TREE-------------------\n\n")
tree.print()
