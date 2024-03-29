from lexical import lexer
from syntax import parser
from semantic import semantic_analyzer


def run(instream):
    res = lexer(instream).gettokens()
    if res[0] == "error":
        res[0] = "lexical error"
        return res
    token_stream, symbol_table = res[1], res[2]
    G, node, statement, parsingtree = parser(token_stream).getparsingtable()
    res = semantic_analyzer(symbol_table, G, node,
                            statement).get_symbol_table()
    if res[0] == "error":
        res[0] = "syntax error"
        return res
    if res[0] == "runtime error":
        return res
    table = ""
    for id in res[1]:
        val = res[1][id]
        if val != {}:
            table = table+id+" = "+str(val)+"\n"
    return table


# print(run("in1.txt"))
