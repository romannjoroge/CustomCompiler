from scanner import Scanner
def getFuncParams(tokens, function_name):
    """
    Get the parameters to the function
    """
    function_calls = []
    for index, token in enumerate(tokens):

        if token[1] == function_name:
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
                            for param in a_func:
                                if param in [
                                    "(",
                                    ")",
                                    function_name,
                                    "int",
                                    "float",
                                    "string",
                                    "boolean",
                                    "(",
                                ]:
                                    a_func.remove(param)
                            return a_func
                        else:
                            break
                            
                    index += 1
    # function_calls = [["$main", "(", "$c", "$d", ")"]]
    # function_definitions = [["$main", "(", "int", "$c", "int", "$d", ")"]]

