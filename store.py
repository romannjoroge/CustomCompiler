from typing import List
def storeTypesData(inputs:List[List]):
    identifier_meta={}
    function_meta={}
    
    for index , input in enumerate(inputs):
        #for identifiers
        #check if type is followed by id
        if input[0]=="TYPE":
           if inputs[index - 1][0] == "ID":
                identifier_name=inputs[index-1][1]
                identifier_type=input[1]
                identifier_meta[identifier_name]={
                        'identifier_type':identifier_type,
                        'identifier_name':identifier_name
                        }
            #for functions check if type is followed by'function'
            #next check for params and store the types.
           elif inputs[index + 1][0] == "function":
                parameter_types=[]
 
                function_name=inputs[index+2][1]
                return_type=input[1]
                if inputs[index+3][1]=="(":
                    while True:
                        if inputs[index][0] == "TYPE" and inputs[index +1][0]=="ID":
                           parameter_types.append(inputs[index][1])
                        if inputs[index][0]==")":
                            function_meta[function_name]={
                                    'return_type':return_type,
                                    'function_name':function_name,
                                    'parameter_types':parameter_types,
                                    }
                            break
                        index+=1
               
    return identifier_meta,function_meta

