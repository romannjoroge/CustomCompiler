from scanner import Scanner
from parser_1 import parserv2
def icg():
    """
    Form the ICG
    """
    tokens = Scanner()
    tree, labels, x = parserv2(tokens, [])
    quadruples  =[]
    temp_variables = 0

    index = 0

    #Go through the tokens from the scanner.
    while index < len(tokens):
        print("Length of tokens", len(tokens))
        print("tokesns", tokens)
        print("index, enterd loop", index)
        print("token", tokens[index])

        # Break if end of input reached
        if tokens[index] == ["$", "$"]:
            print("end of input")
            break

        #For each token:
        token = tokens[index]

        #Look for the position of token in tree
        pos_token = (token[0], index, token[1])
        for key, value in tree.data.items():
            parent = key
            #Handle parent accordingly
            if pos_token in value:
                #check its parent
                print("key: ", key)
                print("pos_token: ", pos_token)

                #Handle parent accordingly
                for val in value:
                    if val[0] == 'AE':
                        T = tree.data[val][0]
                        print("Tree T", T)
                        F = tree.data[T][0]
                        final_value = tree.data[F][0][2]
                        
                        print("Tree vall", tree.data[val])
                        
                        print("final_value", final_value)
                        quad = f"(ASSIGN, {token[1]}, {final_value})"
                        quadruples.append(quad)

                        #Jump to the end of the parent in the token list
                        index = parent[1] + 1
                        print("index", index)
                        break
        
        print("index going to 6", index)
    print("Quadruples: ", quadruples)
                
                
icg()
                
            
        
        