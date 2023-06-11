

class lexer:
    def __init__(self, instream):

        self.instream = instream

        self.digit = []
        for i in range(0, 10):
            self.digit.append(chr(ord('0')+i))

        self.letter = []
        for i in range(0, 26):
            self.letter.append(chr(ord('a')+i))
            self.letter.append(chr(ord('A')+i))

        self.op1 = [';',  '+', '-', '*', '/',
                    "{", "}", "(", ")",]

        self.op2 = ['<', '>', '=']

        self.keywords = ["if", "then", "else", "while", "dollar"]

    def get_token(self, cursor):
        stateu = 0
        string = ""
        i = cursor
        while i < len(self.instream):
            char = self.instream[i]
            statev = self.delta(stateu, char)
            if statev != -1:
                stateu = statev
                string = string+char
                i = i+1
            else:
                return i, stateu
        return i, stateu

    def get_token_stream(self):
        token_stream = []
        symbol_table = {}
        cursor, line, column = 0, 1, 1
        while cursor < len(self.instream):
            char = self.instream[cursor]
            if char in [' ', '\n', '\r', '\t']:
                if char == '\n':
                    line = line+1
                    column = 1
                else:
                    column = column+1
                cursor = cursor+1
            else:
                cursor_, state = self.get_token(cursor)
                if cursor == cursor_:
                    print(token_stream)
                    return ["error", line, column, f"{char} is an unexpected character", cursor, cursor+1]
                else:
                    string = self.instream[cursor:cursor_]
                    if state == 1:
                        if string in self.keywords:
                            token_stream.append(
                                [string, None, line, column, cursor, cursor_])
                        else:
                            token_stream.append(
                                ["ID", string, line, column, cursor, cursor_])
                            symbol_table[string] = {}
                    elif state in [2, 4, 7]:
                        token_stream.append(
                            ["NUM", string, line, column, cursor, cursor_])
                    elif state in [8, 9, 10]:
                        token_stream.append(
                            [string, None, line, column, cursor, cursor_])
                    else:
                        return ["error", line, column, f"\"{string}\" can't be accepted as a legal token.", cursor, cursor_]
                    column = column+len(string)
                    cursor = cursor_

        return ["accept", token_stream, symbol_table]

    def delta(self, stateu, char):
        if stateu == 0:
            if char in self.letter:
                return 1
            if char in self.digit:
                return 2
            if char in self.op2:
                return 8
            if char in self.op1:
                return 10
        if stateu == 1:
            if char in self.letter+self.digit:
                return 1
        if stateu == 2:
            if char in self.digit:
                return 2
            if char == '.':
                return 3
            if char in ['e', 'E']:
                return 5
        if stateu == 3:
            if char in self.digit:
                return 4
        if stateu == 4:
            if char in self.digit:
                return 4
            if char in ['e', 'E']:
                return 5
        if stateu == 5:
            if char in ['+', '-']:
                return 6
            if char in self.digit:
                return 7
        if stateu == 6:
            if char in self.digit:
                return 7
        if stateu == 7:
            if char in self.digit:
                return 7
        if stateu == 8:
            if char == '=':
                return 9
        return -1


if __name__ == "__main__":
    f = open("test.txt")
    instream = f.read()
    print(instream)
    print(lexer(instream).get_token_stream())
