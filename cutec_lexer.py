# The Main CuteC Compiler
# written by Kat Juncker (2026)
# All rights reserved.

import ply.lex as lex

from cutec_types.cutec_type import CutecType


def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

class CuteLexer(object):
    lexer: lex.Lexer | None = None

    reserved = {
        'meow'  : 'MEOW',
        'chase' : 'CHASE',
        'catch' : 'CATCH',
        'escape' : 'ESCAPE',
        'then' : 'THEN',
        'else' : 'ELSE',
        'while' : 'WHILE',
        'for': 'FOR',
        'thing': 'THING',
        'like': 'LIKE',
        'cat': 'CAT',
        'dog': 'DOG',
        'action': 'ACTION',
        'of': 'OF',
        'in': 'IN',
        'to': 'TO',
        'true': 'TRUE',
        'false': 'FALSE',
        'cast': 'CAST',
        'and': 'AND',
        'is': 'IS',
        'or': 'OR',
        'not': 'NOT',
        'switch': 'SWITCH',
        'break': 'BREAK',
        'continue': 'CONTINUE',
        'return': 'RETURN',
        'cpy': 'CPY',
        'mem': 'MEM',
        'keep': 'KEEP',
        'toss': 'TOSS',
        'oops': 'OOPS',
        'import': 'IMPORT',
        'from': 'FORM'
    }

    # List of token names.   This is always required
    tokens = [
        'PLUS',
        'MINUS',
        'TIMES',
        'DIVIDE',
        'MOD',
        'POW',
        'LPAREN',
        'RPAREN',
        'LBRACE',
        'RBRACE',
        'LBRACKET',
        'RBRACKET',
        'DOT',
        'COMMA',
        'ARROW',
        'ASSIGN',
        'COLON',
        'SEMICOLON',
        'NUMBER',
        'TYPE',
        'PRIMITIVE',
        'ID',
        'STRING',
        'CHAR',
        'LT',
        'LTE',
        'GT',
        'GTE',
        'EQ',
        'NEQ',
        'EXCLAM',
        'PIPE',
        'DOUBLE_PIPE'
    ]  + list(reserved.values())

    # Regular expression rules for simple tokens
    t_ARROW = r'->'
    t_LBRACE = r'\{'
    t_RBRACE = r'\}'
    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
    t_COLON = r'\:'
    t_SEMICOLON = r'\;'
    t_PLUS    = r'\+'
    t_MINUS   = r'-'
    t_TIMES   = r'\*'
    t_DIVIDE  = r'/'
    t_MOD = r'\%'
    t_POW = r'\^'
    t_LPAREN  = r'\('
    t_RPAREN  = r'\)'
    t_DOT = r'\.'
    t_COMMA = r','
    t_LTE = r'<='
    t_LT = r'<'
    t_GTE = r'>='
    t_EQ = r'=='
    t_NEQ = r'!='
    t_GT = '>'
    t_ASSIGN = r'='
    t_EXCLAM = r'!'
    t_DOUBLE_PIPE = r'\|\|'
    t_PIPE = r'\|'

    def t_TYPE(self, t):
        r'[A-Z][a-zA-Z_0-9]*'
        return t

    def t_PRIMITIVE(self, t):
        r'(int|float|bool|stack|string|bite)'
        if t.value == 'int':
            t.value = CutecType.Int
        elif t.value == 'float':
            t.value = CutecType.Dbl
        elif t.value == 'bite':
            t.value = CutecType.Char
        elif t.value == 'bool':
            t.value = CutecType.Bool
        elif t.value == 'stack':
            t.value = CutecType.Stack
        elif t.value == 'string':
            t.value = CutecType.Str
        return t

    def t_ID(self, t):
        r'[a-z_][a-zA-Z_0-9]*'
        if t.value in self.reserved:
            t.type = self.reserved.get(t.value)
        else:
            t.type = 'ID'
        return t

    def t_NUMBER(self, t):
        r'-?\d+(\.\d+)?'
        t.value = float(t.value)
        return t

    def t_MULTILINE_COMMENT(self, t):
        r'(/\*(.|\n)*?\*/)|(//.*)'
        pass

    def t_STRING(self, t):
        r'\"([^\\\"]|\\.)*\"'

        # Gotcha 1 Fix: Safely remove exactly one quote from each end
        content = t.value[1:-1]

        # Gotcha 3 Fix: Process escape sequences (optional but usually required)
        try:
            t.value = content.encode('utf-8').decode('unicode_escape')
        except ValueError:
            # Handle malformed escape sequences like \x or \u errors
            print(f"Lexer Error: Malformed escape sequence on line {t.lexer.lineno}")
            t.lexer.skip(1)
            return None

        # PLY Counter: Update lines after processing
        t.lexer.lineno += t.value.count('\n')
        return t

    def t_CHAR(self, t):
        r'\'([^\\\n\']|\\.)\''
        # Gotcha 2 Fix: Slice instead of strip
        content = t.value[1:-1]

        # Process escape sequences (e.g., '\n' becomes an actual newline byte)
        t.value = content.encode('utf-8').decode('unicode_escape')
        return t

    # Define a rule so we can track line numbers
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # A string containing ignored characters (spaces and tabs)
    t_ignore  = ' \t'

    t_ignore_COMMENT = r'\#.*'

    # Error handling rule
    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Build the lexer
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    # Do some lexing!
    def lex(self, data: str):
        self.lexer.input(data)
        toks = []
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            toks.append(tok)
        return toks