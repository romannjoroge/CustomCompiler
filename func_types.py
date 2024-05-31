from scanner import Scanner


def typesinCallmatchDef():
    """
    Arguments types in function call should match the definition.
    """
    # Get the function call
    tokens = Scanner()
    print(list(reversed(tokens)))
    function_calls = []
    function_definitions = []
    for index, token in enumerate(tokens):

        if token[0] == "ID":
            if tokens[index + 1][0] == "(":
                a_func = []
                # print("could be a function call or definition")
                while True:
                    # Get the arguments of the function call || definition
                    a_func.append(tokens[index][1])
                    # print(a_func)
                    if tokens[index][0] == ")":
                        # print(token)
                        # print("Got a close")
                        if tokens[index + 1][0] == ";":
                            function_calls.append(a_func)
                            break
                        else:
                            function_definitions.append(a_func)
                            break
                    index += 1
    # function_calls = [["$main", "(", "$c", "$d", ")"]]
    # function_definitions = [["$main", "(", "int", "$c", "int", "$d", ")"]]

    reversed_tokens = list(reversed(tokens))
    for i_call, call in enumerate(function_calls):
        if call[0] in [definition[0] for definition in function_definitions]:
            new_call = call.copy()
            for i_arg, argument in enumerate(call):

                if argument == call[0] or argument == "(" or argument == ")":
                    continue
                if "$" in argument:

                    for indext, token in enumerate(reversed_tokens):
                        if token[1] == argument:
                            if reversed_tokens[indext - 1][0] != "TYPE":

                                continue
                            elif reversed_tokens[indext - 1][0] == "TYPE":

                                index_of_arg = new_call.index(argument)
                                new_call.insert(
                                    index_of_arg, reversed_tokens[indext - 1][1]
                                )
                                break
                            else:
                                continue
                        else:
                            continue
            if new_call in function_definitions:
                print("Function call matches definition")
            else:
                raise Exception(
                    f"Function call {new_call[0]} does not match definition"
                )
    # Get the corresponding function definition
    # Check if the arguments in the function call match the definition
    # If they don't match, raise an error


typesinCallmatchDef()
