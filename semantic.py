from lexical import lexer
from syntax import parser


class semantic_analyzer:
    def __init__(self, file_path):
        self.token_stream, self.symbol_table = lexer(file_path).gettokens()
        self.parsing_table = parser().getparsingtable()
        self.node = {}
        self.G = {}
        self.statement = {}
        self.synthesized = {}
        self.inherited = {}
        self.build_syntax_tree()
        self.execute(1)

    def get_syntax_tree(self):
        return self.node, self.G

    def get_symbol_table(self):
        return self.symbol_table

    def build_syntax_tree(self):
        stack = [["dollar", 0], ["program", 1]]
        idx = 1
        token_stream = self.token_stream
        while len(stack) and len(token_stream):
            token = stack[-1][0]
            id = stack[-1][1]
            self.node[id] = [token]
            if token == "epsilon":
                del stack[-1]
            elif token == token_stream[0][0]:
                self.node[id] = token_stream[0]
                del stack[-1]
                del token_stream[0]
            elif token_stream[0][0] in self.parsing_table[token]:
                statement = self.parsing_table[token][token_stream[0][0]]
                self.statement[id] = statement
                del stack[-1]
                for i in range(len(statement)-1, 0, -1):
                    stack.append([statement[i], idx+i])
                    if id not in self.G:
                        self.G[id] = []
                    self.G[id].append(idx+len(statement)-i)
                idx = idx + len(statement) - 1

    def execute(self, id):
        if id not in self.G:
            # 终结符
            return
        else:
            # 非终结符
            token = self.node[id][0]
            if token in ["program", "stmt", "stmts", "compoundstmt"]:
                for newid in self.G[id]:
                    self.execute(newid)
            elif token == "ifstmt":
                if self.calculate(self.G[id][2]):
                    self.execute(self.G[id][5])
                else:
                    self.execute(self.G[id][7])
            elif token == "whilestmt":
                while self.calculate(self.G[id][2]):
                    self.execute(self.G[id][4])
            elif token == "assgstmt":
                ID = self.node[self.G[id][0]][1]
                self.symbol_table[ID]["val"] = self.calculate(self.G[id][2])

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
                tmp2 = self.calculate(self.G[id][2])
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
                """
                """
                self.inherited[self.G[id][1]] = self.calculate(self.G[id][0])
                return self.calculate(self.G[id][1])

            elif token in ["arithexprprime", "multexprprime"]:
                if len(self.statement[id]) == 2:
                    return self.inherited[id]
                else:
                    op = self.statement[id][1]
                    if op == '+':
                        tmp1 = self.inherited[id]+self.calculate(self.G[id][1])
                    elif op == '-':
                        tmp1 = self.inherited[id]-self.calculate(self.G[id][1])
                    elif op == '*':
                        tmp1 = self.inherited[id]*self.calculate(self.G[id][1])
                    elif op == '/':
                        tmp1 = self.inherited[id]/self.calculate(self.G[id][1])
                    self.inherited[self.G[id][2]] = tmp1
                    return self.calculate(self.G[id][2])


if __name__ == "__main__":
    symbol_table = semantic_analyzer("in1.txt").get_symbol_table()
    print(symbol_table)
