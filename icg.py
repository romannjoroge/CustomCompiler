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
    
    #Go through the tokens from the scanner.
    #For each token:
    #Look for the position of token in tree
    #check its parent
    #Handle parent accordingly
    #Jump to the end of the parent in the token list
    index = 0
    while index < len(tokens):
        
        print("Length of tokens", len(tokens))
        print("tokesns", tokens)
        print("index, enterd loop", index)
        print("token", tokens[index])
        if tokens[index] == ["$", "$"]:
            print("end of input")
            break
        
        token = tokens[index]
        pos_token = (token[0], index, token[1])
        for key, value in tree.data.items():
            parent = key
            if pos_token in value:
                print("key: ", key)
                print("pos_token: ", pos_token)
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
                        index = parent[1] + 1
                        print("index", index)
                        break
        
        print("index going to 6", index)
    print("Quadruples: ", quadruples)
                
                
icg()
                
            
        
        