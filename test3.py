from scanner import Scanner
from parser_1 import parserv2

tokens = Scanner()
tree, labels = parserv2(tokens, [])
print(f"\n\n----------------TREE-------------------\n\n")

print("Tree is =>", tree.data)

# tree.display()
print(f"\n\nLABELS: \n\n")
for label in labels:
    print(f"{label[1]}\t{label[0]}")
