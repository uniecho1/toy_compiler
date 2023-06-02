
class lex:
    def __init__(self, file_path):
        self.tokens = ["ID", "INTNUM", "REALNUM", "int", "real", ";", "=",
                       "{", "}", "(", ")", "if", "then", "else", "+", "-",
                       "*", "/", ">", "<", "<=", ">=", "=="]

        f = open(file_path)
        self.instream = f.read()
        self.token_table = []
        self.token_stream = []

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
                if 'a' <= string[0] and string[0] <= 'z':  # 是一个 identifier
                    self.token_stream.append(["identifier", string])
                    self.token_table.append([])
            i = j
