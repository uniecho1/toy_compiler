class parser:
    def __init__(self, token_stream):
        self.token_stream = token_stream

        self.grammar = []
        self.grammar.append(["program",  "compoundstmt"])
        self.grammar.append(["stmt", "ifstmt"])
        self.grammar.append(["stmt", "whilestmt"])
        self.grammar.append(["stmt", "assgstmt"])
        self.grammar.append(["stmt", "compoundstmt"])
        self.grammar.append(["compoundstmt", "{", "stmts", "}"])
        self.grammar.append(["stmts", "stmt", "stmts"])
        self.grammar.append(["stmts", "epsilon"])
        self.grammar.append(
            ["ifstmt", "if", "(", "boolexpr", ")", "then", "stmt", "else", "stmt"])
        self.grammar.append(
            ["whilestmt", "while", "(", "boolexpr", ")", "stmt"])
        self.grammar.append(["assgstmt", "ID", "=", "arithexpr", ";"])
        self.grammar.append(["boolexpr", "arithexpr", "boolop", "arithexpr"])
        self.grammar.append(["boolop", "<"])
        self.grammar.append(["boolop", ">"])
        self.grammar.append(["boolop", "<="])
        self.grammar.append(["boolop", ">="])
        self.grammar.append(["boolop", "=="])
        self.grammar.append(["arithexpr", "multexpr", "arithexprprime"])
        self.grammar.append(
            ["arithexprprime", "+", "multexpr", "arithexprprime"])
        self.grammar.append(
            ["arithexprprime", "-", "multexpr", "arithexprprime"])
        self.grammar.append(["arithexprprime", "epsilon"])
        self.grammar.append(["multexpr", "simpleexpr", "multexprprime"])
        self.grammar.append(
            ["multexprprime", "*", "simpleexpr", "multexprprime"])
        self.grammar.append(
            ["multexprprime", "/", "simpleexpr", "multexprprime"])
        self.grammar.append(["multexprprime", "epsilon"])
        self.grammar.append(["simpleexpr", "ID"])
        self.grammar.append(["simpleexpr", "NUM"])
        self.grammar.append(["simpleexpr", "(", "arithexpr", ")"])

        self.isterminal = {}

        for statement in self.grammar:
            self.isterminal[statement[0]] = False

        for statement in self.grammar:
            for token in statement:
                if token not in self.isterminal:
                    self.isterminal[token] = True

        self.first = {}

        for token in self.isterminal:
            self.first[token] = self.getfirst(token)

        self.follow = {}
        for token in self.isterminal:
            if not self.isterminal[token]:
                self.follow[token] = self.getfollow(token, [])
        self.parsing_table = {}
        for statement in self.grammar:
            k = 1
            while k < len(statement):
                for item in self.first[statement[k]]:
                    if item != "epsilon":
                        if statement[0] in self.parsing_table:
                            self.parsing_table[statement[0]][item] = statement
                        else:
                            self.parsing_table[statement[0]] = {
                                item: statement}
                if "epsilon" in self.first[statement[k]]:
                    k = k+1
                else:
                    break
            if k == len(statement):
                for item in self.follow[statement[0]]:
                    if statement[0] in self.parsing_table:
                        self.parsing_table[statement[0]][item] = statement
                    else:
                        self.parsing_table[statement[0]] = {
                            item: statement}

        self.node = {}
        self.statement = {}
        self.G = {}
        self.parsing_tree = ""

    def getfirst(self, cur):
        if cur in self.first:
            return self.first[cur]
        if self.isterminal[cur]:
            self.first[cur] = [cur]
            return self.first[cur]
        res = []
        for statement in self.grammar:
            if statement[0] == cur:
                k = 1
                while k < len(statement):
                    tmp = self.getfirst(statement[k])
                    for item in tmp:
                        res.append(item)
                    if "epsilon" in tmp:
                        k = k+1
                    else:
                        break
        self.first[cur] = res
        return self.first[cur]

    def getfollow(self, cur, stack):
        if cur == "program":
            return ["dollar"]
        stack.append(cur)
        res = []
        for statement in self.grammar:
            for i in range(1, len(statement)):
                if statement[i] == cur:
                    if i+1 < len(statement):
                        k = i+1
                        while k < len(statement):
                            flag = False
                            for item in self.first[statement[k]]:
                                if item != "epsilon" and item not in res:
                                    res.append(item)
                                elif item == "epsilon":
                                    flag = True
                            if flag:
                                k = k+1
                            else:
                                break
                        if k == len(statement) and statement[0] not in stack:
                            tmp = self.getfollow(statement[0], stack)
                            for item in tmp:
                                if item not in res:
                                    res.append(item)
                    elif statement[0] not in stack:
                        tmp = self.getfollow(statement[0], stack)
                        for item in tmp:
                            if item not in res:
                                res.append(item)
        del stack[-1]
        return res

    def build_syntax_tree(self):
        excpt = []
        stack = [["dollar", 0, ["init"]],
                 ["program", 1, ["init"]]]
        tabs = ["", ""]
        idx = 1
        token_stream = self.token_stream
        while len(stack) and len(token_stream):
            token = stack[-1][0]
            id = stack[-1][1]
            # from_statement = stack[-1][2]
            # self.node[id] = [token]
            self.node[id] = [token, None, *token_stream[0][2:]]
            if token == "epsilon":
                self.parsing_tree = self.parsing_tree + \
                    tabs[-1]+token+'\n'
                del tabs[-1]
                del stack[-1]
            elif token == token_stream[0][0]:
                if stack[-1][0] != "dollar":
                    self.parsing_tree = self.parsing_tree + \
                        tabs[-1]+token+'\n'
                self.node[id] = token_stream[0]
                del tabs[-1]
                del stack[-1]
                del token_stream[0]
            elif token in self.parsing_table and token_stream[0][0] in self.parsing_table[token]:
                statement = self.parsing_table[token][token_stream[0][0]]
                self.statement[id] = statement
                tab = tabs[-1]
                self.parsing_tree = self.parsing_tree+tab+token+'\n'
                del tabs[-1]
                del stack[-1]
                for i in range(len(statement)-1, 0, -1):
                    stack.append([statement[i], idx+i, statement])
                    tabs.append(tab+'    ')
                    if id not in self.G:
                        self.G[id] = []
                    self.G[id].append(idx+len(statement)-i)
                idx = idx + len(statement) - 1
            else:
                if token not in self.parsing_table and len(excpt) == 0:
                    return ["error", token_stream[0][2], token_stream[0][3], f"expected \"{token}\", but got {token_stream[0][0]}."]
                else:
                    for item in self.first[token]:
                        if item != "epsilon" and item not in excpt:
                            excpt.append(item)
                    if "epsilon" in self.first[token]:
                        del stack[-1]
                    else:
                        tmp = ""
                        for item in excpt:
                            tmp = tmp+"\""+item+"\""+" "
                        if tmp[-1] == " ":
                            tmp = tmp[:-1]
                        return ["error", token_stream[0][2], token_stream[0][3], f"expected {tmp}, but not \"{token_stream[0][0]}\"."]
        return ["accept"]

    def getparsingtable(self):
        res = self.build_syntax_tree()
        if res[0] == "accept":
            res = res+[self.G, self.node, self.statement, self.parsing_tree]
        return res


if __name__ == "__main__":

    pars = parser()
    for key in pars.first:
        print(f"first({ key }) = {pars.first[key]}")

    for key in pars.first:
        if not pars.isterminal[key]:
            print(f"follow({ key }) = {pars.follow[key]}")

    parsingtable = pars.getparsingtable()
    for nonterminal in parsingtable:
        for terminal in parsingtable[nonterminal]:
            print(nonterminal, terminal, parsingtable[nonterminal][terminal])
