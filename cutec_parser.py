import ply.yacc as yacc

from cutec_ast.action_node import ActionNode
from cutec_ast.assign_node import AssignNode
from cutec_ast.bin_op import BinOp
from cutec_ast.call_node import CallNode
from cutec_ast.catch_node import CatchNode
from cutec_ast.declare_node import DeclareNode
from cutec_ast.escape_node import EscapeNode
from cutec_ast.frame_node import FrameNode
from cutec_ast.chase_node import ChaseNode
from cutec_ast.id_node import IdNode
from cutec_ast.meow_node import MeowNode
from cutec_ast.node import Node
from cutec_ast.param_node import ParamNode
from cutec_ast.scalar_node import ScalarNode
from cutec_ast.thing_node import ThingNode
from cutec_ast.unary_op import UnaryOp
from cutec_lexer import CuteLexer
from cutec_types.cutec_type import CutecType
from cutec_types.primitives import PrimitiveType
from cutec_types.things import ThingType
from cutec_types.type_system import type_system

# Get the token map from the lexer.  This is required.
tokens = CuteLexer.tokens

precedence = (
    ('left', 'MEOW'),
    ('left', 'ESCAPE'),
    ('right', 'ASSIGN'),
    ('right', 'ARROW'),
    ('left', 'OR', 'AND', 'NOT'),
    ('left', 'EQ', 'NEQ', 'LTE', 'LT', 'GT', 'GTE'),
    ('left', 'PLUS', 'MINUS'),    # Medium: standard math addition/subtraction
    ('left', 'TIMES', 'DIVIDE', 'MOD'),  # High: multiplication/division bind tighter
    ('left', 'POW'),
    ('left', 'LPAREN'),
    ('left', 'DOT')
)

def p_cutec(p):
    'cutec : MEOW MEOW expression'
    p[0] = p[3]


def p_statements_list(p):
    'statements : statements statement'
    p[0] = p[1] + [p[2]]

def p_statements_single(p):
    'statements : statement'
    p[0] = [p[1]]

"""
Every statement must make sense and can't just be an arbitrary expression.
For example, a statement can't just be something like A + B as that doesn't 
make any sense and, why should we allow it?

We'll allow:
1. Variable assignments
2. Attribute assignments
3. Action calls (things, standalone)
4. Return statements
5. Exit statements
6. oops statements
7. Chase statements
8. Meow statements  
9. Loops
10. anything else that inherently can perform an action in and of itself and isn't just a value

This is really just to allow our cute syntax for things like:
name/string = 'Bob';
for declaring types in a cute way but not wanting it to ever be mistaken for division lol.

This does mean that CuteC won't allow you to do something like:
x/int = y/int

whereas it would allow you to do:
x/int = y/int = 10

oh no... y/(int = 10)

I guess I'll need to rethink.

x = 
y = 100 over 2
z = (1, 2, and 3)

1 and 2 = [1,2]



"""
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

def p_expression_meow(p):
    'expression : MEOW expression'
    p[0] = MeowNode(p[2])

def p_expression_factor(p):
    'expression : factor'
    p[0] = p[1]

def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]

def p_factor_action(p):
    'factor : action'
    p[0] = p[1]

def p_action(p):
    'action : ACTION LPAREN RPAREN ARROW expression'
    p[0] = ActionNode(p[5])

def p_action_typed(p):
    'action : ACTION LPAREN RPAREN DIVIDE typed ARROW expression'
    p[0] = ActionNode(p[7], None, p[5])

def p_factor_action_with_params(p):
    'action : ACTION LPAREN params RPAREN ARROW expression'
    p[0] = ActionNode(p[6], p[3])

def p_factor_action_with_params_typed(p):
    'action : ACTION LPAREN params RPAREN DIVIDE typed ARROW expression'
    p[0] = ActionNode(p[8], p[3], p[6])

def p_thing_prototype(p):
    'prototype : TYPE ASSIGN thing'
    p[0] = None

def p_factor_thing(p):
    'thing : THING LPAREN attributes RPAREN'
    p[0] = ThingNode(None, p[3])

def p_factor_thing_like(p):
    'thing : THING LIKE TYPE LPAREN attributes RPAREN'
    p[0] = ThingNode(p[3], p[5])

def p_factor_thing_attributes(p):
    'attributes : attributes COMMA attribute'
    p[0] = p[1] + [p[2]]

def p_factor_thing_attributes_single(p):
    'attributes : attribute'
    p[0] = [p[1]]

"""
thing value attributes

Cat = thing (
    name/string, # no default, i.e. emptry string
    age/int = 0,
    color = 'red' # inferred as string
    
    name/string = 'Cat'  
    owner/Human
    name of string, # no default, i.e. emptry string
    age of int = 0,
    color = 'red' # inferred as string,
    
    getName = () -> this.name,
    getName = ()/str -> this.name
    setColor = str(color of string) -> this.color = color
    getSize() -> 'normal'
)
"""

def p_factor_thing_attribute_value(p):
    'attribute : ID ASSIGN attribute_value'
    p[0] = DeclareNode(p[1], None, p[3])

def p_factor_thing_attribute_typed(p):
    'attribute : ID DIVIDE typed'
    p[0] = DeclareNode(p[1], p[3], None)

def p_factor_thing_attribute_value_typed(p):
    'attribute : ID DIVIDE typed ASSIGN attribute_value'
    p[0] = DeclareNode(p[1], p[3], p[5])

def p_thing_attribute_value(p):
    '''attribute_value : scalar
                       | action'''
    p[0] = p[1]

def p_typed(p):
    'typed : simple_type'
    p[0] = p[1]

def p_simple_typed(p):
    'simple_type : PRIMITIVE'
    p[0] = PrimitiveType(p[1].value)

def p_thing_type(p):
    'simple_type : TYPE'
    type_system.register_type(p[1])
    p[0] = ThingType(p[1])

def p_factor_scalar(p):
    'factor : scalar'
    p[0] = p[1]

def p_factor_num(p):
    'scalar : NUMBER'
    p[0] = ScalarNode(CutecType.Dbl, p[1])

def p_factor_id(p):
    'scalar : ID'
    p[0] = IdNode(p[1])

def p_factor_char(p):
    'scalar : CHAR'
    p[0] = ScalarNode(CutecType.Char, p[1])

def p_factor_string(p):
    'scalar : STRING'
    p[0] = ScalarNode(CutecType.Str, p[1])

def p_params(p):
    'params : params COMMA param'
    p[0] = p[1] + [p[3]]

def p_params_single(p):
    'params : param'
    p[0] = [p[1]]

def p_param(p):
    'param : ID DIVIDE typed'
    p[0] = ParamNode(p[1], p[3])

def p_param_with_default_typed_value(p):
    'param : ID DIVIDE typed ASSIGN scalar'
    p[0] = ParamNode(p[1], p[3], p[5])

def p_factor_assign(p):
    'factor : ID ASSIGN expression'
    p[0] = AssignNode(p[1], p[3])

def p_factor_assign_type(p):
    'factor : ID DIVIDE typed ASSIGN expression'
    p[0] = DeclareNode(p[1], p[3], p[5])

def p_factor_declare_type(p):
    'factor : ID DIVIDE typed'
    p[0] = DeclareNode(p[1], p[3], None)

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
    'chase_with_escape : CHASE LPAREN catches COMMA escape RPAREN'
    # Combine catches and the explicit escape clause here
    p[0] = ChaseNode(p[3], p[5])

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
    p[0] = EscapeNode(ScalarNode(CutecType.Int, 0), p[3])

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