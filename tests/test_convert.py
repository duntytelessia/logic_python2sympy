from logic_python2sympy import convert


def test_convert():
    expr = 'not a and (b == 0)'
    assert convert(expr) == 'And(Not(a), Eq(b, 0))'

    expr = 'a or (b < 0) or (0 <= c <= 10)'
    assert convert(expr) == 'Or(a, b < 0, And(0 <= c, c <= 10))'
