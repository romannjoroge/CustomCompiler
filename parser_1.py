from typing import List, Tuple
import pandas as pd
from scanner import Scanner
from tree import Tree, MyTree

parse_df = pd.read_csv("parse_table.csv")
parse_df.head()
parse_df.set_index('STATE', inplace=True)

grammar = []
with open("grammar2.txt", "r") as file:
    text = file.read()
    grammar = text.split("\n")


# return the left hand side of the production
def getLHS(production):
    return production.split("=>")[0].strip()


def getRHS(production):
    return production.split("=>")[1].strip()


trees = []


def parserv2(inputs: List[List], trees) -> MyTree:
    id = 0
    myTree = MyTree()
    labels = []
    # Initialize stacks
    symbol_stack = []
    state_stack = ['S0']

    # For everything in input stream
    # print(inputs)

    """
algorithm :
    variables : one to store identifier types , another for function metadata.

    """
    identifier_meta={}
    function_meta={}
    i = 0
    while i < int(len(inputs)):
        input = inputs[i]
        token = input[0]
        lexeme = input [1]

        # Get action
        top_of_stack = state_stack[-1]
        action = str(parse_df.loc[top_of_stack, token])
        print("Top of stack => ", top_of_stack, "Input token => ", token, "Action => ", action)

        # Shift action
        if action[0] == 'S':
            print(f"\nSHIFT\n",lexeme)

            # Add input token to symbol stack
            symbol_stack.append((token, id))
            labels.append((token, id))

            # Add shifted to state to state stack
            state = f"S{action[1:]}"
            state_stack.append(state)


 


            print("State stack => ", state_stack)
            print("Symbol stack => ", symbol_stack)
            print("Action => ", action, "State => ", state, "Lexeme => ", lexeme)

            i = i + 1
            id = id + 1

        # Reduce action
        elif action[0] == "R":
            print(f"\nREDUCE\n",lexeme)
            # Get production
            rule_number = int(action[1:]) - 1
            production = grammar[rule_number].replace("@", "")
            lhs = getLHS(production)
            rhs = getRHS(production)

            print("LHS => ", lhs, "RHS => ", rhs)
            children: List[Tuple[str, int]] = []
            # Pop both stack as many times as len of rhs
            for k in range(len(rhs.split())):
                state_popped = state_stack.pop()
                symbol_popped = symbol_stack.pop()
                children.append(symbol_popped)
                print(state_popped, "popped from state stack")
                print(symbol_popped, "popped from symbol stack")

            # Push LHS into symbol stack
            id = id + 1
            symbol_stack.append((lhs, id))
            labels.append((lhs, id))
            
            for child in children:
                myTree.add((lhs, id), child)
                
            if lhs=="FUNCTION_DEFINITION":
                func_name=None
                return_type=None
                param_types=[]
                for child in children:
                    token,child_id=child
                    if token=="ID" and func_name is None:
                        func_name=lexeme
                    elif token=="TYPE" and return_type is None:
                        return_type=lexeme
                    #placeholder logic for now
                    elif token=="ARGUMENTS":
                        param_types.append(lexeme)
                function_meta[func_name]={
                    'func_name':func_name,
                    'return_type':return_type,
                    'param_types':param_types,

                    }
            elif lhs=="VARIABLE_DEFINITION":
                id_type=None
                id_name=None
                for child in children:
                    token,child_id=child
                    if token=="ID" and id_name is None:
                        id_name=lexeme
                    elif token=="TYPE" and id_type is None:
                        id_type=lexeme
                identifier_meta[id_name]={
                        'identifier_type':id_type,
                        } 
            # Get go to 
            go_to = parse_df.loc[state_stack[-1], symbol_stack[-1][0]]

            if (type(go_to) is str):
                if("S" not in go_to):
                    go_to_state = "S"+go_to
                else:
                    go_to_state = go_to
            else:
                go_to_state = "S" + str(int(go_to))
                
            print("Go to state => ", go_to_state, "Top of state stack => ", state_stack[-1], "Top of symbol stack => ", symbol_stack[-1])

            # Push state to state stack
            state_stack.append(go_to_state)
            print("State stack => ", state_stack)
            print("Symbol stack => ", symbol_stack)
        
        elif action == "ACCEPT":
            print(f"\n\nSUCCESFULY PARSED!\n\n")
            i = i + 1

        else:
            print(f"\nUNKNOWN STATE\n")
            print("Action => ", action, "Input => ", input, "Token => ", token, "Top of stack => ", state_stack[-1])
            raise Exception(f"Unexpected input {lexeme}")
    print("function_metadata=>",function_meta)
    print("identifier metadata=>",identifier_meta)
    return myTree, labels
