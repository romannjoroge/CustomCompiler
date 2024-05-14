from scanner import Scanner
from parser_1 import my_parse

tokens = Scanner()
tree = my_parse(tokens, [])
print(f"\n\n----------------TREE-------------------\n\n")
tree.print()
