class lexer:
    def __init__(self, instream):
        self.tokens = ["ID", "NUM", ";", "=",
                       "{", "}", "(", ")", "if", "then", "else", "while", "+", "-",
                       "*", "/", ">", "<", "<=", ">=", "==", "dollar"]
        self.keywords = ["if", "then", "else", "while", "dollar"]
        self.instream = instream
        self.cursor = 0
        self.line = 1
        self.column = 1

    def isdigit(self, x):
        return '0' <= x and x <= '9'

    def isalpha(self, x):
        return ('a' <= x and x <= 'z') or ('A' <= x and x <= 'Z')

    def read_intnumber(self, cursor):
        cursor_ = cursor
        while cursor_ <= len(self.instream) and self.isdigit(self.instream[cursor_]):
            cursor_ = cursor_+1
        return cursor_

    def read_fraction(self, cursor):
        return self.read_intnumber(cursor+1)

    def read_exponent(self, cursor):
        if cursor+1 < len(self.instream) and self.instream[cursor+1] in ['-', '+']:
            return self.read_intnumber(cursor+2)
        else:
            return self.read_intnumber(cursor+1)

    def read_keywords_or_identifier(self, cursor):
        cursor_ = cursor
        while cursor_ < len(self.instream) and (self.isdigit(self.instream[cursor_]) or self.isalpha(self.instream[cursor_])):
            cursor_ = cursor_+1
        return cursor_

    def read_operant(self, cursor):
        if cursor < len(self.instream) and self.instream[cursor] in ['{', '}', '(', ')', ';']:
            return cursor + 1
        cursor_ = cursor + 1
        while cursor_ < len(self.instream) and self.instream[cursor_] in ['+', '-', '*', '/', '=', '<', '>']:
            cursor_ = cursor_+1
        return cursor_

    def read_token(self, cursor):
        while cursor < len(self.instream) and self.instream[cursor] in [' ', '\n', '\r', '\t']:
            if self.instream[cursor] == '\n':
                self.line = self.line+1
                self.column = 1
            else:
                self.column = self.column+1
            cursor = cursor+1
        if cursor == len(self.instream):
            return [-1,]
        if self.isdigit(self.instream[cursor]):
            cursor_ = self.read_intnumber(cursor)
            if cursor_ < len(self.instream) and self.instream[cursor_] == '.':
                cursor_ = self.read_fraction(cursor_)
                if cursor_ < len(self.instream) and self.instream[cursor_] in ['e', 'E']:
                    cursor_ = self.read_exponent(cursor_)
            elif cursor_ < len(self.instream) and self.instream[cursor_] in ['e', 'E']:
                cursor_ = self.read_exponent(cursor_)
            cursor_ = min(cursor_, len(self.instream))
            return ["NUM", self.instream[cursor: cursor_], self.line, self.column, cursor, cursor_]

        elif self.isalpha(self.instream[cursor]):
            # keywords / identifier
            cursor_ = self.read_keywords_or_identifier(cursor)
            tmp = self.instream[cursor: cursor_]
            if tmp in self.keywords:
                return [tmp, None, self.line, self.column, cursor, cursor_]
            else:
                return ["ID", tmp, self.line, self.column, cursor, cursor_]
        else:
            # operants
            cursor_ = self.read_operant(cursor)
            return [self.instream[cursor:cursor_], None, self.line, self.column, cursor, cursor_]

    def check_token(self, token):
        if token[0] == "ID":
            return len(token[1]) <= 63
        if token[0] == "NUM":
            try:
                float(token[1])
            except ValueError:
                return False
            else:
                return True
        else:
            return token[0] in self.tokens[2:]

    def get_token_stream(self):
        token_stream = []
        symbol_table = {}
        while self.cursor < len(self.instream):
            token = self.read_token(self.cursor)
            # print(token)
            if token[0] == -1:
                break
            if not self.check_token(token):
                return ["error", token[2], token[3], f"\"{token[1]}\" can't be accepted as a legal token.", token[4], token[5]]
            token_stream.append(token)
            if token[0] == "ID" and token[1] not in symbol_table:
                symbol_table[token[1]] = {}
            self.cursor = token[-1]
            self.column = self.column+token[-1]-token[-2]
        return ["accept", token_stream, symbol_table]


if __name__ == "__main__":
    f = open("test.txt")
    instream = f.read()+" dollar"
    # print(instream)
    print(lexer(instream).get_token_stream())
