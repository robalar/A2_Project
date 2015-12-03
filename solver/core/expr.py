from collections import deque
from structs import ASTNode
from symbol import Symbol

__author__ = 'Robert Hales'


class Operator(object):

    def __init__(self, symbol, precedence, association):
        self.symbol = symbol
        self.precedence = precedence
        self.association = association

    def __repr__(self):
        return self.symbol


Pow = Operator('**', 4, 'right')
Mul = Operator('*', 3, 'left')
Div = Operator('/', 3, 'left')
Add = Operator('+', 2, 'left')
Min = Operator('-', 2, 'left')


def shunting_yard(tokens):

    """
    An implementation of Edsger Dijkstra's shunting-yard algorithm from the psudo-code here:
        https://en.wikipedia.org/wiki/Shunting-yard_algorithm
    """

    out_queue = deque()
    op_stack = []

    for token in tokens:
        # If the token is a number...
        if isinstance(token, (int, float, Symbol)):
            out_queue.append(token) # ...add it to the output queue

        # If the token is an operator...
        elif isinstance(token, Operator):
            # While there is an operator in the stack...
            while op_stack and isinstance(op_stack[-1], Operator):
                top_operator = op_stack[-1]
                # ...if token is left-associative and its precedence is <= to that of the top operator...
                if (token.association == 'left' and token.precedence <= top_operator.precedence or
                        # ...if the token is right associative, and has precedence less than that of the top operator...
                        token.association == 'right' and token.precedence < top_operator.precedence):
                    # ... pop it from the stack and push it to the queue
                    out_queue.append(op_stack.pop())
                    continue
                break

            op_stack.append(token)

        # If token is a left parenthesis...
        elif token == '(':
            # ...push it to the queue
            op_stack.append('(')

        # If the token is a right parenthesis
        elif token == ')':
            # Until the the operator at the top of the stack is a left parenthesis...
            while op_stack and not op_stack[-1] == '(':
                # ...pop operators off the stack onto the output queue
                out_queue.append(op_stack.pop())
            # Pop the left parenthesis from the stack (but not onto the queue)
            op_stack.pop()

    # After all tokens are read...
    while op_stack:
        if op_stack[-1] == '(' or op_stack[-1] == ')':
            raise Exception('Mismatched parenthesis in expression ')
        out_queue.append(op_stack.pop())

    return list(out_queue)


def rpn_to_ast(rpn_list):

    stack = []

    for token in rpn_list:
        if isinstance(token, (int, float, Symbol)):
            stack.append(ASTNode(token))
        elif isinstance(token, Operator):
            b = stack.pop()
            a = stack.pop()
            stack.append(ASTNode(token, a, b))

    return stack[0]


def build_expression_ast(token_list):
    return rpn_to_ast(shunting_yard(token_list))
