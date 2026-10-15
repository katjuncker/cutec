# The Main CuteC Compiler
# written by Kat Juncker (2026)
# All rights reserved.

import ply.lex as lex

# Compute column.
#     input is the input text string
#     token is a token instance
def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

reserved = {
   'if' : 'IF',
   'then' : 'THEN',
   'else' : 'ELSE',
   'while' : 'WHILE'
}

# List of token names.   This is always required
tokens = [
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'LBRACKET',
    'RBRACKET',
    'DOT',
    'ARROW',
    'ASSIGN',
    'COLON',
    'SEMICOLON',
    'ID',
    'STRING',
    'CHAR',
    'LT',
    'LTE',
    'GT',
    'GTE'
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
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_DOT = r'\.'
t_LTE = r'<='
t_LT = r'<'
t_GTE = r'>='
t_GT = '>'
t_ASSIGN = r'='

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

# A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_MULTILINE_COMMENT(t):
    r'(/\*(.|\n)*?\*/)|(//.*)'
    pass

def t_STRING(t):
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
    print(t.value, len(t.value))
    return t

def t_CHAR(t):
    r'\'([^\\\n\']|\\.)\''
    # Gotcha 2 Fix: Slice instead of strip
    content = t.value[1:-1]

    # Process escape sequences (e.g., '\n' becomes an actual newline byte)
    t.value = content.encode('utf-8').decode('unicode_escape')
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

t_ignore_COMMENT = r'\#.*'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Test it out
data = '''
x: string = "mulit
line
string";
y: char = 'c';
# a comment
/* a 
multi-line
comment
*/
x >= 5
'''
# input('Write a test program: ')

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break      # No more input
    print(tok)