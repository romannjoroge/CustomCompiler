from scanner import Scanner


def getfuncArgs(tokens, function_name):
    """
    Get the arguments of a function
    """
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
                            for val in a_func:
                                if val in [
                                    "(",
                                    ")",
                                    function_name,
                                    "int",
                                    "float",
                                    "string",
                                    "boolean",
                                    "(",
                                ]:
                                    a_func.remove(val)
                                
                            break
                        else:
                            for val in a_func:

                                if val in [
                                    "(",
                                    ")",
                                    function_name,
                                    "int",
                                    "float",
                                    "string",
                                    "boolean",
                                    "(",
                                ]:

                                    a_func.remove(val)
                            return a_func
                    index += 1
