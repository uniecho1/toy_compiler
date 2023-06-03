from lexical import lexer
from syntax import parser

file_path = "in.txt"

token_stream, token_table = lexer(file_path).gettokens()
token_stream.append(["dollar"])
parsing_table = parser().getparsingtable()

stack = ["dollar", "program"]


while len(stack) and len(token_stream):
    print(stack)
    print(token_stream)
    print()
    if stack[-1] == token_stream[0][0]:
        del stack[-1]
        del token_stream[0]
    elif token_stream[0][0] in parsing_table[stack[-1]]:
        statement = parsing_table[stack[-1]][token_stream[0][0]]
        del stack[-1]
        for i in range(len(statement)-1, 0, -1):
            if statement[i] != "epsilon":
                stack.append(statement[i])
