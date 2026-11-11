import ply.yacc as yacc

from cutec_ast.action_node import ActionNode
from cutec_ast.assign_node import AssignNode
from cutec_ast.bin_op import BinOp
from cutec_ast.call_node import CallNode
from cutec_ast.catch_node import CatchNode
from cutec_ast.escape_node import EscapeNode
from cutec_ast.frame_node import FrameNode
from cutec_ast.chase_node import ChaseNode
from cutec_ast.id_node import IdNode
from cutec_ast.node import Node
from cutec_ast.param_node import ParamNode
from cutec_ast.scalar_node import ScalarNode
from cutec_ast.unary_op import UnaryOp
from cutec_lexer import CuteLexer

# Get the token map from the lexer.  This is required.
tokens = CuteLexer.tokens

precedence = (
    ('left', 'ARROW'),  # Lowest precedence
    ('left', 'ESCAPE'),
    ('right', 'ASSIGN'),
    ('right', 'ARROW'),             # Lowest: allows the lambda body to stretch as far as possible
    ('left', 'OR', 'AND', 'NOT'),
    ('left', 'EQ', 'NEQ', 'LTE', 'LT', 'GT', 'GTE'),
    ('left', 'PLUS', 'MINUS'),    # Medium: standard math addition/subtraction
    ('left', 'TIMES', 'DIVIDE', 'MOD'),  # High: multiplication/division bind tighter
    ('left', 'POW'),
    ('left', 'LPAREN'),
    ('left', 'DOT')
)

def p_cutec(p):
    'cutec : expression'
    p[0] = p[1]


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

def p_expression_mod(p):
    'expression : expression MOD expression'
    p[0] = BinOp('%', p[1], p[3])

def p_expression_pow(p):
    'expression : expression POW expression'
    p[0] = BinOp('^', p[1], p[3])

def p_expression_dot(p):
    'expression : expression DOT ID'
    p[0] = BinOp('.', p[1], p[3])

def p_expression_eq(p):
    'expression : expression EQ expression'
    p[0] = BinOp('==', p[1], p[3])

def p_expression_neq(p):
    'expression : expression NEQ expression'
    p[0] = BinOp('!=', p[1], p[3])

def p_expression_gt(p):
    'expression : expression GT expression'
    p[0] = BinOp('>', p[1], p[3])

def p_expression_gte(p):
    'expression : expression GTE expression'
    p[0] = BinOp('>=', p[1], p[3])

def p_expression_lt(p):
    'expression : expression LT expression'
    p[0] = BinOp('<', p[1], p[3])

def p_expression_lte(p):
    'expression : expression LTE expression'
    p[0] = BinOp('<=', p[1], p[3])

def p_expression_and(p):
    'expression : expression AND expression'
    p[0] = BinOp('and', p[1], p[3])

def p_expression_or(p):
    'expression : expression OR expression'
    p[0] = BinOp('or', p[1], p[3])

def p_expression_not(p):
    'expression : NOT expression'
    p[0] = UnaryOp('not', p[2])

def p_expression_factor(p):
    'expression : factor'
    p[0] = p[1]

def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]

def p_factor_action(p):
    'factor :  ACTION LPAREN RPAREN ARROW expression'
    p[0] = ActionNode(p[5])

def p_factor_action_with_params(p):
    'factor :  ACTION LPAREN params RPAREN ARROW expression'
    p[0] = ActionNode(p[5])

def p_factor_scalar(p):
    'factor : scalar'
    p[0] = p[1]

def p_factor_num(p):
    'scalar : NUMBER'
    p[0] = ScalarNode('number', p[1])

def p_factor_id(p):
    'scalar : ID'
    p[0] = IdNode(p[1])

def p_factor_char(p):
    'scalar : CHAR'
    p[0] = ScalarNode('char', p[1])

def p_factor_string(p):
    'scalar : STRING'
    p[0] = ScalarNode('string', p[1])

def p_params(p):
    'params : params COMMA param'
    p[0] = p[1] + [p[3]]

def p_params_single(p):
    'params : param'
    p[0] = [p[1]]

def p_param(p):
    'param : ID'
    p[0] = ParamNode(p[1])

def p_param_with_default(p):
    'param : ID ASSIGN scalar'
    p[0] = ParamNode(p[1], p[3])

def p_factor_assign(p):
    'factor : ID ASSIGN expression'
    p[0] = AssignNode(p[1], p[3])

def p_factor_object_assign(p):
    'factor : expression DOT ID ASSIGN expression'
    p[0] = AssignNode(p[3], p[5], p[1])

def p_factor_call_empty(p):
    'factor : expression LPAREN RPAREN'
    p[0] = CallNode(p[1])

def p_factor_call_list(p):
    'factor : expression LPAREN argument_list RPAREN'
    p[0] = CallNode(p[1], p[3])

def p_argument_list(p):
    'argument_list : argument_list COMMA expression'
    p[0] = p[1] + [p[3]]

def p_argument_list_expression(p):
    'argument_list : expression'
    p[0] = [p[1]]

def p_expression_chase_with_escape(p):
    'expression : chase_with_escape'
    p[0] = p[1]

def p_expression_chase_no_escape(p):
    'expression : chase_no_escape'
    p[0] = p[1]

def p_chase_with_escape(p):
    'chase_with_escape : CHASE LPAREN catches escape RPAREN'
    # Combine catches and the explicit escape clause here
    p[0] = ChaseNode(p[3], p[4])

def p_chase_no_escape(p):
    'chase_no_escape : CHASE LPAREN catches RPAREN'
    # Default case when no escape block is specified
    p[0] = ChaseNode(p[3])

def p_catches_multi(p):
    'catches : catches COMMA catch'
    p[0] = p[1] + [p[3]]

def p_catches_catch(p):
    'catches : catch'
    p[0] = [p[1]]

def p_catch(p):
    'catch : expression ARROW expression'
    p[0] = CatchNode(p[1], p[3])

def p_escape(p):
    'escape : ESCAPE ARROW expression'
    p[0] = EscapeNode(ScalarNode('number', 0), p[3])

def p_escape_timeout(p):
    'escape : ESCAPE LPAREN expression RPAREN ARROW expression'
    p[0] = EscapeNode(p[3], p[6])

def p_expr_frame(p):
    'expression : LBRACE statements RBRACE'
    p[0] = FrameNode(p[2])

def p_empty(p):
    'empty :'
    p[0] = None  # Or any default value like False or ''

# Error rule for syntax errors
def p_error(p):
    if p:
        print(f"Syntax error at token: {p.type}, value: {p.value!r}")
        print(f"Line: {p.lineno}, position: {p.lexpos}")
    else:
        print("Syntax error at EOF")

# # Build the lexer
# lexer = CuteLexer()
# lexer.build()
#
# # Build the parser
# parser = yacc.yacc()

class CutecParser:
    def __init__(self):
        # Build the lexer
        self.lexer = CuteLexer()
        self.lexer.build()

        # Build the parser
        self.parser = yacc.yacc(debug=True, write_tables=True)

    def parse(self, cutec_code: str) -> Node | None:
        return self.parser.parse(cutec_code, lexer=self.lexer.lexer)