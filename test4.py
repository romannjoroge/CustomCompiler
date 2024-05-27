from scanner import Scanner
from parser_1 import parserv2
from allIdentifiersMustBeDefined import allIdentifiersMustBeDefined

tokens = Scanner()
tree, labels = parserv2(tokens, [])
print(f"\n\n----------------TREE-------------------\n\n")

print("Tree is =>", tree.data)

print(f"\nSEMANTIC ANALYSIS\n")
# Check if variable definition is there
allIdentifiersMustBeDefined(tokens=tokens, tree=tree)
print("All Identifiers are used after being defined")  