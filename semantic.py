class semantic_analyzer:
    def __init__(self, token_stream, symbol_table, parsing_table, first):
        self.token_stream = token_stream
        self.symbol_table = symbol_table
        self.parsing_table = parsing_table
        self.first = first
        self.node = {}
        self.G = {}
        self.statement = {}
        self.synthesized = {}
        self.inherited = {}

    # def get_syntax_tree(self):
    #     return self.node, self.G

    def get_symbol_table(self):
        res = self.build_syntax_tree()
        if res[0] == "error":
            return res
        tmp = self.execute(1)
        if type(tmp) == list and tmp[0] == "error":
            tmp[0] = "runtime error"
            return tmp+["divide 0 happend"]
        return ["accept", self.symbol_table]

    def build_syntax_tree(self):
        excpt = []
        stack = [["dollar", 0, ["init"]],
                 ["program", 1, ["init"]]]
        idx = 1
        token_stream = self.token_stream
        while len(stack) and len(token_stream):
            token = stack[-1][0]
            id = stack[-1][1]
            # from_statement = stack[-1][2]
            # self.node[id] = [token]
            self.node[id] = [token, None, *token_stream[0][2:]]
            if token == "epsilon":
                del stack[-1]
            elif token == token_stream[0][0]:
                self.node[id] = token_stream[0]
                del stack[-1]
                del token_stream[0]
            elif token in self.parsing_table and token_stream[0][0] in self.parsing_table[token]:
                statement = self.parsing_table[token][token_stream[0][0]]
                self.statement[id] = statement
                del stack[-1]
                for i in range(len(statement)-1, 0, -1):
                    stack.append([statement[i], idx+i, statement])
                    if id not in self.G:
                        self.G[id] = []
                    self.G[id].append(idx+len(statement)-i)
                idx = idx + len(statement) - 1
            else:
                if token not in self.parsing_table and len(excpt) == 0:
                    return ["error", token_stream[0][2], token_stream[0][3], f"expected {token}, but got {token_stream[0][0]}."]
                else:
                    for item in self.first[token]:
                        if item != "epsilon" and item not in excpt:
                            excpt.append(item)
                    if "epsilon" in self.first[token]:
                        del stack[-1]
                    else:
                        return ["error", token_stream[0][2], token_stream[0][3], f"expected {excpt}, but not {token_stream[0][0]}"]
        return ["accept"]

    def execute(self, id):
        if id not in self.G:
            # 终结符
            return "accept"
        else:
            # 非终结符
            token = self.node[id][0]
            if token in ["program", "stmt", "stmts", "compoundstmt"]:
                for newid in self.G[id]:
                    tmp = self.execute(newid)
                    if type(tmp) == list and tmp[0] == "error":
                        return tmp
            elif token == "ifstmt":
                tmp = self.calculate(self.G[id][2])
                if type(tmp) == list and tmp[0] == "error":
                    return tmp
                if tmp:
                    self.execute(self.G[id][5])
                else:
                    self.execute(self.G[id][7])
            elif token == "whilestmt":
                while True:
                    tmp = self.calculate(self.G[id][2])
                    if type(tmp) == list and tmp[0] == "error":
                        return tmp
                    if not tmp:
                        break
                    self.execute(self.G[id][4])
            elif token == "assgstmt":
                ID = self.node[self.G[id][0]][1]
                tmp = self.calculate(self.G[id][2])
                if type(tmp) == list and tmp[0] == "error":
                    return tmp
                self.symbol_table[ID]["val"] = tmp
            return "accept"

    def calculate(self, id):
        token = self.node[id][0]
        if id not in self.G:
            # 终结符
            if token == "NUM":
                return float(self.node[id][1])
            elif token == "ID":
                ID = self.node[id][1]
                if "val" in self.symbol_table[ID]:
                    return self.symbol_table[ID]["val"]
                else:
                    print("error uninitialized")
            elif token in ["<", ">", "<=", ">=", "=="]:
                return token
        else:
            # 非终结符
            if token == "simpleexpr":
                if len(self.statement[id]) <= 2:
                    return self.calculate(self.G[id][0])
                else:
                    return self.calculate(self.G[id][1])
            elif token == "boolop":
                return self.calculate(self.G[id][0])
            elif token == "boolexpr":
                tmp1 = self.calculate(self.G[id][0])
                if type(tmp1) == list and tmp1[0] == "error":
                    return tmp1
                tmp2 = self.calculate(self.G[id][2])
                if type(tmp2) == list and tmp2[0] == "error":
                    return tmp2
                op = self.calculate(self.G[id][1])
                if op == "<":
                    return tmp1 < tmp2
                elif op == ">":
                    return tmp1 > tmp2
                elif op == "<=":
                    return tmp1 <= tmp2
                elif op == ">=":
                    return tmp1 >= tmp2
                elif op == "==":
                    return tmp1 == tmp2
            elif token in ["arithexpr", "multexpr"]:
                tmp = self.calculate(self.G[id][0])
                if type(tmp) == list and tmp[0] == "error":
                    return tmp
                self.inherited[self.G[id][1]] = tmp
                return self.calculate(self.G[id][1])
            elif token in ["arithexprprime", "multexprprime"]:
                if len(self.statement[id]) == 2:
                    return self.inherited[id]
                else:
                    op = self.statement[id][1]
                    tmp2 = self.calculate(self.G[id][1])
                    if type(tmp2) == list and tmp2[0] == "error":
                        return tmp2
                    if op == '+':
                        tmp1 = self.inherited[id]+tmp2
                    elif op == '-':
                        tmp1 = self.inherited[id]-tmp2
                    elif op == '*':
                        tmp1 = self.inherited[id]*tmp2
                    elif op == '/':
                        if tmp2 == 0:
                            return ["error", *self.node[id][2:]]
                        tmp1 = self.inherited[id]/tmp2
                    self.inherited[self.G[id][2]] = tmp1
                    return self.calculate(self.G[id][2])


if __name__ == "__main__":
    symbol_table = semantic_analyzer("in1.txt").get_symbol_table()
    print(symbol_table)
