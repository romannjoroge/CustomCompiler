from scanner import Scanner
from parser_1 import parserv2

tokens = Scanner()
tree, labels, x = parserv2(tokens, [])
print(f"\n\n----------------TREE-------------------\n\n")

for key, value in tree.data.items():
    print(f"{key} -> {value}")
    

# tree.display()
# print(f"\n\nLABELS: \n\n")
# for label in labels:
#     print(f"{label[1]}\t{label[0]}")
