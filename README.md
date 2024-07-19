# logic_python2sympy

`Sympy` has the advantage of using `Python` syntax in its own expressions, but with some exceptions :
logical expressions in `Sympy` differ a bit from their `Python` counterparts (`a and b` is written `a & b` in `Sympy`).
Thus, this module provides functions that can convert a logical expression written in `Python` syntax, into a `Sympy` expression.

## Usage

```python
>>> import logic_python2sympy as p2s
>>> code = "not a and ((x > 0) or (y != 0))"
>>> print(p2s.convert(code))
And(Not(a), Or((x > 0), Neq(y, 0)))
```

### convert

```python
convert(expr: str) -> str
```

Transform a `Python` logical expression into `Sympy` syntax. \
expr: valid logical expression, i.e. expr must be valid `Python` syntax, and must be a combintion of the following `ast` nodes: `BoolOp, BinOp, UnaryOp, Compare, Call, Constant, Name` \
raises: `NotImplentedError`
