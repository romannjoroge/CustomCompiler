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
    i = 0
    while i < int(len(inputs) / 2):
        input = inputs[i]
        token = input[0]
        lexeme = input [1]

        # Get action
        top_of_stack = state_stack[-1]
        action = str(parse_df.loc[top_of_stack, token])
        print("Top of stack => ", top_of_stack, "Input token => ", token, "Action => ", action)

        # Shift action
        if action[0] == 'S':
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
            print(f"\nREDUCE\n")
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
            
    return myTree, labels





def parse(inputs: List[List], trees) -> Tree:
    # Keep track of states
    newTree = Tree()
    state_stack = ['S0']

    i = 0
    while i < len(inputs):
        input = inputs[i]
        # Get the action (get item at row with state and column of input)
        top_of_stack = state_stack[-1]
        token = input[0]
        lexeme = input[1]

        if (type(top_of_stack) is not str):
            top_of_stack = "S" + str(int(top_of_stack))

        if ("S" not in top_of_stack):
            top_of_stack = 'S'+top_of_stack

        print("Top of stack => ", top_of_stack, "Token => ", token)
        action = str(parse_df.loc[top_of_stack, token])

        # If action is shift, shift
        if action[0] == 'S':
            # Append the token
            state_stack.append(token)
            # Append new state
            state = f"S{action[1:]}"
            state_stack.append(state)
            # Add a tree to list of trees
            tree = Tree()
            tree.data = lexeme
            trees.append(tree)
            print("Action => ", action, "State => ", state, "Lexeme => ", lexeme)
            i = i + 1

        # If action is reduce
        # Reduce
        elif action[0] == 'R':
            rule_number = int(action[1:]) - 1
            # Get the production for the rule we are reducing
            production = grammar[rule_number].replace("@", "")
            lhs = getLHS(production)
            rhs = getRHS(production)

            print("Rule number => ", rule_number, "LHS =>", lhs, "RHS => ", rhs)

            # Pop the stack 2 times the number of items at RHS of production
            num_items = len(rhs.split())
            for j in range(num_items * 2):
                popped_item = state_stack.pop()
                print("Popped Item => ", popped_item)

            # Put at top of stack LHS of production
            prev_top_of_stack = state_stack[-1]
            state_stack.append(lhs)

            # Put at top of stack the goto of previous top of stack and LHS of production
            new_top_item = parse_df.loc[prev_top_of_stack, lhs]
            print("Prev Top of state => ", prev_top_of_stack, "LHS => ", lhs, "New Top => ", new_top_item)
            state_stack.append(new_top_item)

            # create a new tree and set data to lhs
            newTree = Tree()
            newTree.data = lhs

            # get "len(rhs)" trees from the right of the list of trees and add
            # each of them as child of the new tree you created, preserving
            # the left-right order
            for tree in trees[-len(rhs):]:
                newTree.add(tree)

            # remove "len(rhs)" trees from the right of the list of trees
            trees = trees[:-len(rhs)]

            # append the new tree to the list of trees
            trees.append(newTree)
            
            
        # implement the "accept" operation
        else:
            # set lhs as the start symbol; assume that the lhs of the 1st 
            # production has the start symbol
            production = grammar[0]
            lhs = getLHS(production)

            # reduce all trees to the start symbol
            newTree = Tree()
            newTree.data = lhs
            for tree in trees:
                newTree.add(tree)

            i = i + 1
            print()

    # For each input
    # for input in inputs:
    #     # Get the action (get item at row with state and column of input)
    #     top_of_stack = state_stack[-1]
    #     token = input[0]
    #     lexeme = input[1]

    #     if (type(top_of_stack) is not str):
    #         top_of_stack = "S" + str(int(top_of_stack))

    #     if ("S" not in top_of_stack):
    #         top_of_stack = 'S'+top_of_stack

    #     print("Top of stack => ", top_of_stack, "Token => ", token)
    #     action = str(parse_df.loc[top_of_stack, token])

    #     print("Action => ", action, "Token => ", token, "Input => ", input, "Lexeme => ", lexeme)

    #     # If action is shift, shift
    #     if action[0] == 'S':
    #         # Append the token
    #         state_stack.append(token)
    #         # Append new state
    #         state = f"S{action[1:]}"
    #         state_stack.append(state)
    #         # Add a tree to list of trees
    #         tree = Tree()
    #         tree.data = lexeme
    #         trees.append(tree)

    #     # If action is reduce
    #     # Reduce
    #     elif action[0] == 'R':
    #         rule_number = int(action[1:]) - 1
    #         # Get the production for the rule we are reducing
    #         production = grammar[rule_number].replace("@", "")
    #         lhs = getLHS(production)
    #         rhs = getRHS(production)

    #         print("Rule number => ", rule_number, "LHS =>", lhs, "RHS => ", rhs)

    #         # Pop the stack 2 times the number of items at RHS of production
    #         num_items = len(rhs.split())
    #         for i in range(num_items * 2):
    #             popped_item = state_stack.pop()
    #             print("Popped Item => ", popped_item)

    #         # Put at top of stack LHS of production
    #         prev_top_of_stack = state_stack[-1]
    #         state_stack.append(lhs)

    #         # Put at top of stack the goto of previous top of stack and LHS of production
    #         new_top_item = parse_df.loc[prev_top_of_stack, lhs]
    #         print("Prev Top of state => ", prev_top_of_stack, "LHS => ", lhs, "New Top => ", new_top_item)
    #         state_stack.append(new_top_item)

    #         # create a new tree and set data to lhs
    #         newTree = Tree()
    #         newTree.data = lhs

    #         # get "len(rhs)" trees from the right of the list of trees and add
    #         # each of them as child of the new tree you created, preserving
    #         # the left-right order
    #         for tree in trees[-len(rhs):]:
    #             newTree.add(tree)

    #         # remove "len(rhs)" trees from the right of the list of trees
    #         trees = trees[:-len(rhs)]

    #         # append the new tree to the list of trees
    #         trees.append(newTree)
            
            
    #     # implement the "accept" operation
    #     else:
    #         # set lhs as the start symbol; assume that the lhs of the 1st 
    #         # production has the start symbol
    #         production = grammar[0]
    #         lhs = getLHS(production)

    #         # reduce all trees to the start symbol
    #         newTree = Tree()
    #         newTree.data = lhs
    #         for tree in trees:
    #             newTree.add(tree)
    #         print()

    # return the new tree
    return newTree

tokens=Scanner()



def loadSLR(input):
    actions={}
    gotos={}
    tokens=[]
    header = input.readline().strip().split(",")
    end=header.index("S0")
    for field in header[1:end]:
        tokens.append(int(field))
    #tokens.append(int(Token.EOF))   # '$' is replaced by token 0
    variables = header[end + 1:]
    for line in input:
        row = line.strip().split(",")
        state = int(row[0])
        for i in range(len(tokens)):
            token = tokens[i]
            key = (state, token)
            value = row[i + 1]
            if len(value) == 0:
                value = None
            actions[key] = value
        for i in range(len(variables)):
            variable = variables[i]
            key = (state, variable)
            value = row[i + len(tokens) + 1]
            if len(value) == 0:
                value = None
            gotos[key] = value
    return (actions, gotos)


