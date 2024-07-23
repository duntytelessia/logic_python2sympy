from logic_python2sympy import get_expression
from sympy import symbols, Eq, simplify


def test_get_expression():
    a, b, c = symbols('a b c')
    expr = 'not a and (b == 0)'
    sol = ~a & Eq(b, 0)
    assert simplify(get_expression(expr)) == simplify(sol)

    expr = 'a or (b < 0) or (0 <= c <= 10)'
    sol = a | (b < 0) | ((0 <= c) & (c <= 10))
    assert simplify(get_expression(expr)) == simplify(sol)
