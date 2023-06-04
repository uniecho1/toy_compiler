class parser:
    def __init__(self):
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

    def getparsingtable(self):
        return self.parsing_table


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
