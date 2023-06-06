from lexical import lexer
from syntax import parser
from semantic import semantic_analyzer


def run(file_path):
    res = lexer(file_path).gettokens()
    if res[0] == "error":
        res[0] = "lexical error"
        return res
    token_stream, symbol_table = res[1], res[2]
    parsing_table, first = parser().getparsingtable()
    res = semantic_analyzer(token_stream, symbol_table,
                            parsing_table, first).get_symbol_table()
    if res[0] == "error":
        res[0] = "syntax error"
        return res
    if res[0] == "runtime error":
        return res
    return res[1]


print(run("in1.txt"))
