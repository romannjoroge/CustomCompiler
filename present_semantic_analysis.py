from allIdentifiersMustBeDefined import allIdentifiersMustBeDefined
from scanner import Scanner
from parser_1 import parserv2

tokens = Scanner()
tree, labels = parserv2(tokens, [])
allIdentifiersMustBeDefined(tree=tree, tokens=tokens)
