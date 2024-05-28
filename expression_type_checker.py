from typing import List, Dict, Any, Tuple
from tree import MyTree

def getExpressionType(tree: MyTree, node: Tuple[str, int], identifier_meta: Dict[str, Dict[str, Any]]) -> str:
    node_label, node_position = node
    children = tree.data.get(node, [])

    if node_label == "EXPRESSION":
        if len(children) == 1:
            return getExpressionType(tree, children[0], identifier_meta)
        elif len(children) == 3:
            left_type = getExpressionType(tree, children[0], identifier_meta)
            operator = children[1][0]
            right_type = getExpressionType(tree, children[2], identifier_meta)

            if left_type == right_type:
                return left_type
            else:
                raise Exception(f"Type mismatch in expression at {node_position}: {left_type} and {right_type}")

    elif node_label == "TERM":
        if len(children) == 1:
            return getExpressionType(tree, children[0], identifier_meta)

    elif node_label == "FACTOR":
        if len(children) == 1:
            child_label, child_position = children[0]
            if child_label == "NUMBER":
                return "int"
            elif child_label == "ID":
                identifier = child_position[1]  # Assuming child_position is (token, position)
                if identifier in identifier_meta:
                    return identifier_meta[identifier]['identifier_type']
                else:
                    raise Exception(f"Undefined identifier {identifier} at position {child_position}")
        elif len(children) == 3:
            return getExpressionType(tree, children[1], identifier_meta)

    return "Unknown"
def checkExpressionTypes(tree: MyTree, identifier_meta: Dict[str, Dict[str, Any]]):
    for node, children in tree.data.items():
        if isinstance(node, tuple) and len(node) == 2:
            node_label, node_position = node
            if node_label == "EXPRESSION":
                try:
                    expr_type = getExpressionType(tree, node, identifier_meta)
                    print(f"Expression at position {node_position} has type {expr_type}")
                except Exception as e:
                    print(e)
        else:
            print(f"Node format: {node}")

