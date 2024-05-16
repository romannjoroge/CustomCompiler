from scanner import Scanner
from parser_1 import parserv2

tokens = Scanner()
tree = parserv2(tokens, [])
print(f"\n\n----------------TREE-------------------\n\n")
tree.print()
