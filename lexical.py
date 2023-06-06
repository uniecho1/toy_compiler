
class lexer:
    def __init__(self, file_path):
        self.tokens = ["ID", "NUM", "int", "real", ";", "=",
                       "{", "}", "(", ")", "if", "then", "else", "while", "+", "-",
                       "*", "/", ">", "<", "<=", ">=", "=="]

        f = open(file_path)
        self.instream = f.read()
        self.symbol_table = {}
        self.token_stream = []

    def isintnum(self, string):
        for item in string:
            if item < '0' or item > '9':
                return False
        return True

    def isrealnum(self, string):
        cnt = 0
        pos = -1
        for i in range(len(string)):
            if string[i] == '.':
                cnt = cnt+1
                pos = i
        if cnt != 1 or pos == 0 or pos+1 == len(string):
            return False
        tmp1, tmp2 = string.split('.')
        if self.isintnum(tmp1) and self.isintnum(tmp2):
            return True
        else:
            return False

    def isnum(self, string):
        cnt = 0
        pos = -1
        for i in range(len(string)):
            if string[i] in ['E', 'e']:
                cnt = cnt+1
                pos = i
        if cnt > 1 or pos == 0 or pos+1 == len(string):
            return False
        if cnt == 0:
            return self.isintnum(string) or self.isrealnum(string)
        else:
            tmp1, tmp2 = string.split("e")
            if tmp2[0] == '+' or tmp2[0] == '-':
                del tmp2[0]
            return (self.isintnum(tmp1) or self.isrealnum(tmp1)) and self.isintnum(tmp2)

    def gettokens(self):
        line = 1
        column = 1
        i = 0
        while i < len(self.instream):
            while i < len(self.instream) and self.instream[i] in [' ', '\n', '\r', '\t']:
                i = i + 1
                if i == '\n':
                    line = line+1
                    column = 1
                elif i == '\t':
                    column = column+4
                else:
                    column = column+1
            j = i
            while j < len(self.instream) and self.instream[j] not in [' ', '\n', '\r', '\t']:
                j = j+1
            string = self.instream[i:j]
            flag = False
            for k in range(2, len(self.tokens)):
                if string == self.tokens[k]:
                    self.token_stream.append([string, None, line, column])
                    flag = True
            if not flag:
                if 'a' <= string[0] and string[0] <= 'z':  # identifier
                    self.token_stream.append(["ID", string, line, column])
                    if string not in self.symbol_table:
                        self.symbol_table[string] = {}
                elif self.isnum(string):
                    self.token_stream.append(["NUM", string, line, column])
                else:
                    return ["error", line, column, string]
            column = column+len(string)
            i = j

        return ["accept", self.token_stream, self.symbol_table]


if __name__ == "__main__":
    lexer = lexer("in1.txt")
    print(lexer.gettokens())
