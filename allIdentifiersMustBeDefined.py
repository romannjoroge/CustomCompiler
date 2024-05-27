from typing import List
from tree import MyTree

def allIdentifiersMustBeDefined(tokens: List[List], tree: 'MyTree'):
    defined_identifiers = []
    # Look through code and get where an identifier is used
    for index, token in enumerate(tokens):
        if token[0] == "ID":
            identifier = token[1]
            # Check if identifier has already been defined
            if identifier in defined_identifiers:
                # Identifier is good
                continue
            else:
                # Check if variable is currently being defined
                is_identifier_being_defined = checkIfIdetifierIsBeingDefined(tree, identifier, index)
                if is_identifier_being_defined == False:
                    raise Exception(f"Identifier {identifier} is used before being defined")
                else:
                    defined_identifiers.append(identifier)
        else:
            continue
    pass

def checkIfIdetifierIsBeingDefined(tree: 'MyTree', lexeme: str, position: int) -> bool:
    # Loop through tree data
    for key, value in tree.data.items():
        # Check if item is a variable definition
        if 'VARIABLE_DEFINITION' in key:
            # Check if identifier is one of the children
            for child in value:
                if "ID" in child and lexeme in child:
                    # Check if position is the same
                    if position == child[1]:
                        return True
                    else:
                        continue
                else:
                    continue
        else:
            continue
    return False