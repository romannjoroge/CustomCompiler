from scanner import Scanner
from parser_1 import parserv2


def icg():
    """
    Form the ICG
    """
    tokens = Scanner()
    tree, labels = parserv2(tokens, [])
    quadruples = []
    temp_variables = 0
    label_vars = 0

    index = 0

    # Go through the tokens from the scanner.
    while index < len(tokens):
        print("Length of tokens", len(tokens))
        print("tokesns", tokens)
        print("index, enterd loop", index)
        print("token", tokens[index])

        # Break if end of input reached
        if tokens[index] == ["$", "$"]:
            print("end of input")
            break

        # For each token:
        token = tokens[index]

        # Look for the position of token in tree
        pos_token = (token[0], index, token[1])
        for key, value in tree.data.items():
            parent = key
            # Handle parent accordingly
            if pos_token in value:
                # check its parent
                print("key: ", key)
                print("pos_token: ", pos_token)
                if key[0] == "VARIABLE_DEFINITION":
                    print("handling VARIABLE_DEFINITION")
                    # Handle parent accordingly
                    for val in value:

                        # Variable definition
                        if val[0] == "AE":
                            T = tree.data[val][0]
                            print("Tree T", T)
                            F = tree.data[T][0]
                            final_value = tree.data[F][0][2]

                            print("Tree vall", tree.data[val])

                            print("final_value", final_value)
                            quad = f"(ASSIGN, {token[1]}, {final_value})"
                            quadruples.append(quad)

                            # Jump to the end of the parent in the token list
                            index = parent[1] + 1
                            print("index", index)
                            break

                # Handling assignment
                if key[0] == "ASSIGNMENT":
                    print(" handling ASSIGNMENT")
                    for val in value:
                        # Handle assignment
                        # eg. (ASSIGN, $d, 4)
                        if val[0] == "INT" or val[0] == "FLOAT" or val[0] == "STR":
                            quad = f"(ASSIGN, {token[1]}, {val[2]})"
                            quadruples.append(quad)
                            index = parent[1] + 1
                            break

                        # Handles assignment for AE
                        if val[0] == "AE":
                            T = tree.data[val][0]
                            F = tree.data[T][0]
                            final_value = tree.data[F][0][2]

                            quad = f"(ASSIGN, {token[1]}, {final_value})"
                            quadruples.append(quad)

                            # Jump to the end of the parent in the token list
                            index = parent[1] + 1
                            break

                # Handle if
                if key[0] == "IF":
                    print("handling IF")
                    if token[0] == "}":
                        quad = f"(GOTO, {label})"
                        quadruples.append(quad)
                        quad = f"(LABEL, {label})"
                        quadruples.append(quad)

                        # Creating key for else portion
                        our_else = ("ELSE", parent[1])
                        # Checking if else portion has any members
                        if len(tree.data[our_else]) > 0:
                            # TODO handle body
                            print(
                                "ELSE portionfweffffffff@@@@@@",
                                tree.data[our_else],
                            )
                            for open_brack in tree.data[our_else]:
                                    if open_brack[0] == "{":
                                        index = open_brack[1] + 1
                                        print("index@@#############", index)
                                        break
                        else:
                            index = parent[1] + 1

                    else:
                        for val in value:
                            # Handle the logical expression in IF
                            if val[0] == "LE":
                                le1 = tree.data[val][0]
                                le2 = tree.data[le1][0]
                                le3 = tree.data[le2][0]
                                le4 = tree.data[le3][0]
                                le5 = tree.data[le4][0]

                                # Creating temp variables to store IF logical expression
                                if_expression = tree.data[le5][0][2]
                                temp = f"t{temp_variables}"
                                temp_variables += 1
                                quad = f"(ASSIGN, {temp}, {if_expression})"
                                quadruples.append(quad)

                                # Temp variable to store negation of if expression
                                temp2 = f"t{temp_variables}"
                                temp_variables += 1
                                quad = f"(NOT, {temp2}, {temp})"
                                quadruples.append(quad)

                                # Creating label for the code in else or that which is executed if there is no if
                                label = f"L{label_vars}"
                                quad = f"(IF, {temp2}, {label})"
                                quadruples.append(quad)

                                # TODO:Handle the body
                                for open_brack in value:
                                    if open_brack[0] == "{":
                                        index = open_brack[1] + 1
                                        print("index@@#############", index)
                                        break
                if key[0] == "ELSE":
                    if token[0] == "}":
                        index = parent[1] + 1
                        print("index##$$ELSE", index)
                    
                    
                                        
                                

                # Handle while
                if key[0] == "WHILE_LOOP":
                    print("handling WHILE")
                    if token[0] == "}":
                        quad = f"(GOTO, {label})"
                        quadruples.append(quad)
                        index = parent[1] + 1
                    else:
                        for val in value:
                            # Handling the logical expression in WHILE
                            if val[0] == "LE":
                                le1 = tree.data[val][0]
                                le2 = tree.data[le1][0]
                                le3 = tree.data[le2][0]
                                le4 = tree.data[le3][0]
                                le5 = tree.data[le4][0]

                                # Creating temp variables to store IF logical expression
                                le_expression = tree.data[le5][0][2]
                                label = f"L{label_vars}"
                                label_vars += 1
                                quad = f"(LABEL, {label})"
                                quadruples.append(quad)
                                temp = f"t{temp_variables}"
                                temp_variables += 1
                                quad = f"(ASSIGN, {temp}, {le_expression})"
                                quadruples.append(quad)

                                # Temp variable to store negation of if expression
                                temp2 = f"t{temp_variables}"
                                temp_variables += 1
                                quad = f"(NOT, {temp2}, {temp})"
                                quadruples.append(quad)

                                # Creating label for the code in else or that which is executed if there is no if
                                label2 = f"L{label_vars}"
                                quad = f"(IF, {temp2}, {label2})"
                                label_vars += 1
                                quadruples.append(quad)
                                for open_brack in value:
                                    if open_brack[0] == "{":
                                        index = open_brack[1] + 1
                                        print("index@@#############", index)
                                        break

                                # We go to start of the while loop

        print("index going to {}".format(index))
    print("Quadruples: ", quadruples)


icg()
