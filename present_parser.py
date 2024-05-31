from scanner import Scanner
from parser_1 import parserv2

# Scan
tokens = Scanner()

# Parse
tree, labels = parserv2(tokens, [])

# Display tree used in semantic analysis
print("\nTREE:\n")
for key, value in tree.data.items():
    print(f"{key} -> {value}")

# Display labels
print("\nLABELS:\n")
for label in labels:
    print(f"{label[1]} => {label[0]}")

tree.display()
