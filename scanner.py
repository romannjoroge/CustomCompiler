import re
from typing import List 
tokens = []  # store tokens
def add_space(source_code):
  # Add space before and after special characters
  source_code = re.sub(r'([^\w\s$])', r' \1 ', source_code)
  return source_code

def Scanner() -> List[List]:
    """
    Contains the logic for scanning the source code
    """
    #open file and read the words
  #open file and read the words
    with open('source.txt', 'r') as file:
        source_code = file.read()
        source_code = add_space(source_code)
        source_code = source_code.split()
        #used to store the words that are then joined to form the complete strnig literal.
        possible_string = []
        #flagging if a string literal is present or not
        saw_string = False
        saw_function = False
        saw_open_curly = False
        saw_close_curly = False
        seen_function_keyword = False
        collected_words = []
        seen_open_curly = False

    # Loop through each source code word
    for word in source_code:
      if seen_function_keyword is True:
        if seen_open_curly is False:
          # Go through all words as you store them till you find something
          # that has {
          if not re.match(r'.*{\s*$', word):
            collected_words.append(word)
          else:
            collected_words.append(word)
            seen_open_curly = True
        else:
          seen_identifier = False
          concatendated_words = "".join(collected_words)

          # Check for identifier
          if re.match(r"^\$[a-zA-Z_][a-zA-Z0-9_]*\s*\(", concatendated_words):
            # Extract identifier from concatenated words and add it as well as ( in tokens
            result = re.search(r'^\$[a-zA-Z_][a-zA-Z0-9_]*', concatendated_words)
            if (result):
              identifier = result.group(0)
              tokens.append(["ID", identifier])
              tokens.append(["(", "("])

              words_without_identifier = concatendated_words.replace(
                  identifier + '(', "")
              # See if there are arguements and if so add them to token stream
              arguement_search = re.search(r'.*\)', words_without_identifier)
              if (arguement_search):
                arguements = arguement_search.group(0).replace(")", "")

                # Extract individual arguements
                args = []
                if len(arguements) > 0:
                  args = arguements.split(",")

                if len(args) == 0:
                  tokens.append([")", ")"])
                  # Look for closing brace
                  words_without_arguements = words_without_identifier.replace(
                      arguement_search.group(0), "")
                  open_brace_search = re.search(r'^\s*{\s*$',
                                                words_without_arguements)
                  if (open_brace_search):
                    tokens.append(["{", "{"])
                  else:
                    print("No open brace found")
                else:
                  # check if each argument is valid
                  for arg in args:
                    arg_valid_search = re.search(
                        r'^(int|string|float|boolean)\$[a-zA-Z_][a-zA-Z0-9_]*$',
                        arg)
                    if (arg_valid_search):
                      found_arg = arg_valid_search.group(0)

                      identifier_arg_search = re.search(
                          r"\$[a-zA-Z_][a-zA-Z0-9_]*$", found_arg)
                      if (identifier_arg_search):
                        ident = identifier_arg_search.group(0)
                        type = found_arg.replace(identifier_arg_search.group(0),
                                                 "")
                        tokens.append(["TYPE", type])
                        tokens.append(
                            ["ID",
                             identifier_arg_search.group(0)])
                    else:
                      tokens.append(["INVALID_TOKEN", arg])
                      print("Invalid arguemnt", arg)

                  tokens.append([")", ")"])
                  # Look for closing brace
                  words_without_arguements = words_without_identifier.replace(
                      arguement_search.group(0), "")
                  open_brace_search = re.search(r'^\s*{\s*$',
                                                words_without_arguements)
                  if (open_brace_search):
                    tokens.append(["{", "{"])
                    seen_function_keyword = False
                  else:
                    print("No open brace found")
              else:
                tokens.append(["INVALID_TOKEN", words_without_identifier])
                print("Function Not Closed", words_without_identifier)
            else:
              print("Could Not Get Identifier")

            seen_function_keyword = False
            collected_words = []
            seen_open_curly = False
          else:
            raise Exception("Expected function name idenifier but got:",
                            concatendated_words)

      elif saw_string is True:
        #if the current word ends with a quote then it is
        #a string literal else appends the word to the #possible_string list.
        if re.match(r'.*"$', word):
          possible_string.append(" " + word)
          string = "".join(possible_string)
          possible_string = []
          tokens.append(["STR", string])
          #show string literal has ended
          saw_string = False
        else:

          possible_string.append(" " + word)

      else:
        # This will check if a token has datatype decleration
        if word in ['string', 'int', 'boolean', 'float']:
          tokens.append(['TYPE', word])

        elif re.match(r'^".*', word):
          saw_string = True
          possible_string.append(word)

        #this will look for a keyword
        elif word == 'false':
          tokens.append(['false', word])
        elif word == 'true':
          tokens.append(['true', word])

        elif word == 'if':
          tokens.append(['if', word])

        elif word == 'else':
          tokens.append(['else', word])

        elif word == 'function':
          tokens.append(['function', word])
          seen_function_keyword = True


        elif word == 'while':
          tokens.append(['while', word])

        elif word == 'return':
          tokens.append(['return', word])

        elif word == ';':
          tokens.append([';', word])
        # This will look for an identifier which would be just a word
        elif re.match("^\\$[a-zA-Z_][a-zA-Z0-9_]*$", word):
          tokens.append(['ID', word])

        # This will look for an operator
        elif word == "*":
          tokens.append(["*" , word])

        elif word == "-":
          tokens.append(["-" , word])

        elif word == "/":
          tokens.append(["/" , word])

        elif word == "+":
          tokens.append(["+" , word])

        elif word == "=":
          tokens.append(["=" , word])

        elif word == "()":
          tokens.append(['(', "("])
          tokens.append([')', ")"])

        elif word == "{}":
          tokens.append(['{', "{"])
          tokens.append(['}', "}"])

        # curly braces ,brackets and parenthesis
        elif word == '{':
          tokens.append(['{', word])

        elif word == '}':
          tokens.append(['}', word])

        elif word == '(':
          tokens.append(['(', word])

        elif word == ")":
          tokens.append([')', word])

        # logical operators
        elif word in '&|':
          tokens.append(['LOGICAL_OPERATOR', word])

        # comparison operators
        elif word in '==':
          tokens.append(['==', word])
        elif word in '!=':
          tokens.append(['!=', word])
        elif word in '<':
          tokens.append(['<', word])
        elif word in '>':
          tokens.append(['>', word])
        elif word in '!':
          tokens.append(['!', word])
      # elif re.match(r"([^\"\\]|\\[\s\S])*", word):
      #r"([^\"\\]|\\.)*"
      #elif re.match(r"([^\"\\]|\\[\s\S])*", word):
      # tokens.append(['STRING', word])

      # This will look for integer items and cast them as a number
        elif re.match(r'^[0-9]([0-9])*$', word):
          if word[len(word) - 1] == ';':
            tokens.append(["INT", word[:-1]])
            tokens.append([';', ';'])
          else:
            tokens.append(["INT", word])
          # r'^[-+]?[0-9]*\.[0-9]+$'  r'^-?\d+(\.\d+)?$'' r'^[0-9]([0-9]*)\.([0-9]*)$'
        elif re.match(r'[0-9]([0-9])*\.[loadTable0-9]*$', word):
          if word[len(word) - 1] == ';':
            tokens.append(["FLOAT", word[:-1]])
            tokens.append([';', ';'])
          else:
            tokens.append(["FLOAT", word])

        else:
          tokens.append(["INVALID_TOKEN", word])
    return tokens
