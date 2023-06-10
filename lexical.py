
class lexer:
    def __init__(self, instream):
        self.tokens = ["ID", "NUM", "int", "real", ";", "=",
                       "{", "}", "(", ")", "if", "then", "else", "while", "+", "-",
                       "*", "/", ">", "<", "<=", ">=", "==", "dollar"]

        # f = open(file_path)
        self.instream = instream
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
                tmp2 = tmp2[1:]
            return (self.isintnum(tmp1) or self.isrealnum(tmp1)) and self.isintnum(tmp2)

    def isletter(self, c):
        return ('a' <= c and c <= 'z') or ('A' <= c and c <= 'Z')

    def isdigit(self, c):
        return '0' <= c and c <= '9'

    def gettokens(self):
        line = 1
        column = 1
        i = 0
        while i < len(self.instream):
            while i < len(self.instream) and self.instream[i] in [' ', '\n', '\r', '\t']:
                if self.instream[i] == '\n':
                    line = line+1
                    column = 1
                elif self.instream[i] == '\t':
                    column = column+1
                else:
                    column = column+1
                i = i + 1
            if i == len(self.instream):
                break
            j = i
            while j < len(self.instream) and self.instream[j] not in [' ', '\n', '\r', '\t']:
                j = j+1
            string = self.instream[i:j]
            flag = False
            for k in range(2, len(self.tokens)):
                if string == self.tokens[k]:
                    self.token_stream.append(
                        [string, None, line, column, i, j])
                    flag = True
            if not flag:
                if self.isletter(string[0]):  # identifier
                    if len(string) > 64:
                        return ["error", line, column, f"\"{string}\" is too long."]
                    for item in string:
                        if not self.isdigit(item) and not self.isletter(item):
                            return ["error", line, column, f"\"{string}\" can't be accepted as a legal token."]
                    self.token_stream.append(
                        ["ID", string, line, column, i, j])
                    if string not in self.symbol_table:
                        self.symbol_table[string] = {}
                elif self.isnum(string):
                    self.token_stream.append(
                        ["NUM", string, line, column, i, j])
                else:
                    return ["error", line, column, f"\"{string}\" can't be accepted as a legal token."]
            column = column+len(string)
            i = j

        return ["accept", self.token_stream, self.symbol_table]


if __name__ == "__main__":
    f = open("in2.txt")
    instream = f.read()+" dollar"
    # print(instream)
    print(lexer(instream).gettokens())
