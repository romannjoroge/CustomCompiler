from allIdentifiersMustBeDefined import allIdentifiersMustBeDefined
from func_types import typesinCallmatchDef
from scanner import Scanner
from store import storeTypesData
from parser_1 import parserv2

tokens = Scanner()
identifier_metadata,function_metadata=storeTypesData(tokens)
print(" collected identifier information=>",identifier_metadata)
print("Collected function information=>",function_metadata)
tree, labels = parserv2(tokens, [])
allIdentifiersMustBeDefined(tree=tree, tokens=tokens)
typesinCallmatchDef()
