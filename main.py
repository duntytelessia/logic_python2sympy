import ast
import astor
import sympy
from typing import Any
from transformer import Transformer


def convert(expr: str) -> str:
    '''
    Transform a `Python` logical expression into `Sympy` syntax.
    expr: valid logical expression, i.e. expr must be valid `Python` syntax,
    and must be a combintion of the following `ast` nodes:
    `BoolOp, BinOp, UnaryOp, Compare, Call, Constant, Name`
    raises: `NotImplentedError`, when the expression contains operators that are not supported in `Sympy`
    '''

    tree = ast.parse(expr)
    transformer = Transformer()
    new_tree = transformer.visit(tree)
    return astor.to_source(new_tree)


def get_expression(expr: str) -> Any:
    '''
    Transform a `Python` logical expression into a `Sympy` expression.
    expr: valid logical expression, i.e. expr must be valid `Python` syntax,
    and must be a combintion of the following `ast` nodes:
    `BoolOp, BinOp, UnaryOp, Compare, Call, Constant, Name`
    raises: `NotImplentedError`, when the expression contains operators that are not supported in `Sympy`
    '''

    new_expr = convert(expr)
    return sympy.sympify(new_expr)


if __name__ == '__main__':
    expr = '0 < x <= 10 and y != 0'
    print(get_expression(expr))
