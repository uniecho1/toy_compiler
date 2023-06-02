
class lex:
    def __init__(self, file_path):
        self.tokens = ["ID", "INTNUM", "REALNUM", "int", "real", ";", "=",
                       "{", "}", "(", ")", "if", "then", "else", "+", "-",
                       "*", "/", ">", "<", "<=", ">=", "=="]

        f = open(file_path)
        self.instream = f.read()
        self.token_table = []
        self.token_stream = []

    def isnum(self, string):
        cnt = 0
        for i in range(len(string)):
            c = string[i]
            if not ('0' <= c and c <= '9' or c == '.'):
                return False
            cnt = cnt + (c == '.')
            if c == '.' and (i == 0 or i+1 == len(string)):
                return False
        return cnt <= 1

    def gettokens(self):
        for i in range(len(self.instream)):
            while i < len(self.instream) and self.instream[i] in [' ', '\n', '\r', '\t']:
                i = i + 1
            j = i
            while j < len(self.instream) and self.instream[j] not in [' ', '\n', '\r', '\t']:
                j = j+1
            string = self.instream[i:j]
            flag = False
            for k in range(3, len(self.tokens)):
                if string == self.tokens[k]:
                    self.token_stream.append(string)
                    flag = True
            if not flag:
                if 'a' <= string[0] and string[0] <= 'z':  # identifier
                    self.token_stream.append(["identifier", string])
                    if string not in self.token_table:
                        self.token_table.append(string)
                elif self.isnum(string):
                    if '.' in string:  # realnum
                        self.token_stream.append(["realnum", string])
                    else:
                        self.token_stream.append(["intnum", string])
                else:
                    "trigger error"
            i = j
        return self.token_stream, self.token_table
