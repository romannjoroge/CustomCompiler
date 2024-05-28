from scanner import Scanner
from parser_1 import parserv2
from allIdentifiersMustBeDefined import allIdentifiersMustBeDefined, getListOfArguements

tokens = Scanner()
tree, labels = parserv2(tokens, [])
print(f"\n\n----------------TREE-------------------\n\n")

print("Tree is =>", tree.data)

print(f"\nSEMANTIC ANALYSIS\n")

# Test if getListOfArguements works
# arguements = getListOfArguements(function_def_position=18, tree=tree)
# print("Gotten arguements is => ", arguements)

# Check if variable definition is there
allIdentifiersMustBeDefined(tokens=tokens, tree=tree)
print("All Identifiers are used after being defined")  