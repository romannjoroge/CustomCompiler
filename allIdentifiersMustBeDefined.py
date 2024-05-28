from typing import List, Tuple
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
        # Check if item is a function definition
        elif 'FUNCTION_DEFINITION' in key:
            # Check if identifier is one of the children
            for child in value:
                # Check if the identifier is the name of the function
                if "ID" in child and lexeme in child:
                    # Check if position is the same
                    if position == child[1]:
                        return True
                    else:
                        continue
                
                # Check if its one of the arguements
                else:
                    # Get arguements
                    arguements = getListOfArguements(function_def_position=key[1], tree=tree)
                    for arg in arguements:
                        if arg[0] == lexeme and arg[1] == position:
                            return True
                        else:
                            continue
        else:
            continue
    return False

def getListOfArguements(function_def_position: int, tree: 'MyTree') -> List[Tuple[str, int]]:
    # Get the function definition
    for key, value in tree.data.items():
        # Check if item is the function definition we are looking for
        if 'FUNCTION_DEFINITION' in key and function_def_position in key:
            # Get the arguements child
            arguements_child = ()
            for child in value:
                if 'ARGUMENTS' in child:
                    arguements_child = child

                    # Get children of arguements child
                    arguement_children = tree.data[arguements_child]

                    # If children is empty
                    if len(arguement_children) == 0:
                        return []
                    else:
                        arguements = []
                        for entry in arguement_children:
                            if "ID" in entry:
                                arguements.append((entry[2], entry[1]))
                        return arguements
                else:
                    continue
        else:
            continue

    return []