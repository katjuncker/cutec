from cutec_lexer import CuteLexer

# Build the lexer
m = CuteLexer()

m.build()

toks = m.lex('''
x: Binary = mem(1024)
keep x
toss x
''')

print(toks)