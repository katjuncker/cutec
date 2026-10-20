import ply.yacc as yacc

from cutec_ast.action_node import ActionNode
from cutec_ast.assign_node import AssignNode
from cutec_ast.bin_op import BinOp
from cutec_ast.call_node import CallNode
from cutec_ast.frame_node import FrameNode
from cutec_ast.scalar_node import ScalarNode
from cutec_lexer import CuteLexer

# Get the token map from the lexer.  This is required.
tokens = CuteLexer.tokens

precedence = (
    ('right', 'ASSIGN'),
    ('right', 'ARROW'),             # Lowest: allows the lambda body to stretch as far as possible
    ('left', 'PLUS', 'MINUS'),    # Medium: standard math addition/subtraction
    ('left', 'TIMES', 'DIVIDE'),  # High: multiplication/division bind tighter
    ('left', 'LPAREN')
)

def p_cutec(p):
    'cutec : statements'
    p[0] = p[1]

def p_frame(p):
    'frame : LBRACE statements RBRACE'
    p[0] = FrameNode(p[1])

def p_statements_list(p):
    'statements : statements statement'
    p[0] = p[1] + [p[2]]

def p_statements_single(p):
    'statements : statement'
    p[0] = [p[1]]

def p_statement(p):
    'statement : expression SEMICOLON'
    p[0] = p[1]

def p_expression_plus(p):
    'expression : expression PLUS expression'
    p[0] = BinOp('+', p[1], p[3])

def p_expression_minus(p):
    'expression : expression MINUS expression'
    p[0] = BinOp('-', p[1], p[3])

def p_expression_times(p):
    'expression : expression TIMES expression'
    p[0] = BinOp('*', p[1], p[3])

def p_expression_divide(p):
    'expression : expression DIVIDE expression'
    p[0] = BinOp('/', p[1], p[3])

def p_expression_factor(p):
    'expression : factor'
    p[0] = p[1]

def p_factor_num(p):
    'factor : NUMBER'
    p[0] = ScalarNode('number', p[1])

def p_factor_id(p):
    'factor : ID'
    p[0] = p[1]

def p_factor_char(p):
    'factor : CHAR'
    p[0] = ScalarNode('char', p[1])

def p_factor_string(p):
    'factor : STRING'
    p[0] = ScalarNode('string', p[1])

def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]

def p_factor_action(p):
    'factor :  ACTION LPAREN RPAREN frame'
    p[0] = ActionNode(p[4])

def p_factor_action_lambda(p):
    'factor :  ACTION LPAREN RPAREN ARROW expression'
    p[0] = ActionNode(FrameNode([p[5]]))

def p_factor_assign(p):
    'factor : ID ASSIGN expression'
    p[0] = AssignNode(p[1], p[3])

def p_factor_call_empty(p):
    'factor : expression LPAREN RPAREN'
    p[0] = CallNode(p[1], p[3])

def p_factor_call_list(p):
    'factor : expression LPAREN argument_list RPAREN'
    p[0] = CallNode(p[1], p[3])

def p_argument_list(p):
    'argument_list : argument_list COMMA expression'
    p[0] = p[1] + [p[3]]

def p_argument_list_expression(p):
    'argument_list : expression'
    p[0] = [p[1]]


# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the lexer
lexer = CuteLexer()
lexer.build()

# Build the parser
parser = yacc.yacc()

while True:
   try:
       s = input('cutec > ' )
   except EOFError:
       break
   if not s: continue
   result = parser.parse(s, lexer=lexer.lexer)
   print(result)