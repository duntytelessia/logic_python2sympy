'''
This module contains the overwritten `ast.NodeTransfomer` class
used to transform the AST
'''
import ast


class Transformer(ast.NodeTransformer):
    '''
    Node transformer used to convert `Python` logic syntax into `Sympy` logic syntax
    This class will only take a combination of the following nodes (ast.BoolOp, ast.BinOp,
    ast.UnaryOp, ast.Compare, ast.Call, ast.Constant, ast.Name); an error will be raised if
    any other node is encountered.
    '''

    AUTHORIZED_NODES = (
        ast.Module,
        ast.Expr,
        ast.BoolOp,
        ast.BinOp,
        ast.UnaryOp,
        ast.Compare,
        ast.Call,
        ast.Constant,
        ast.Name,
        ast.Load,
        ast.keyword
    )

    def visit(self, node: ast.AST) -> ast.AST:
        if not isinstance(node, self.AUTHORIZED_NODES):
            raise ValueError(f"{node.__class__.__name__} node is not supported.")

        return super().visit(node)

    def visit_BoolOp(self, node: ast.BoolOp) -> ast.Call:

        values = [self.visit(v) for v in node.values]

        match node.op:

            case ast.Or():
                return ast.Call(ast.Name('Or'), values, [])

            case ast.And():
                return ast.Call(ast.Name('And'), values, [])

    def visit_BinOp(self, node: ast.BinOp) -> ast.AST:

        left = self.visit(node.left)
        right = self.visit(node.right)

        if isinstance(node.op, (ast.MatMult, ast.LShift, ast.RShift, ast.BitOr, ast.BitXor, ast.BitAnd)):
            error = NotImplementedError(f"Sympy does not support the {node.op.__class__.__name__} operator, "
                                        f"so the transformation is impossible.")
            raise error

        return ast.BinOp(left, node.op, right)

    def visit_UnaryOp(self, node: ast.UnaryOp) -> ast.AST:

        operand = self.visit(node.operand)

        if isinstance(node.op, ast.Not):
            return ast.Call(ast.Name('Not'), [operand], [])
        else:
            return ast.UnaryOp(node.op, operand)

    def visit_Compare(self, node: ast.Compare) -> ast.AST:

        left = self.visit(node.left)
        comparators = [self.visit(c) for c in node.comparators]
        expressions = [left] + comparators
        new_expressions = []

        length = len(node.ops)
        for i in range(length):
            match node.ops[i]:

                case ast.Eq():
                    expr = ast.Call(ast.Name('Eq'), expressions[i:i+2], [])
                    new_expressions.append(expr)

                case ast.NotEq():
                    expr = ast.Call(ast.Name('Ne'), expressions[i:i+2], [])
                    new_expressions.append(expr)

                case ast.Lt():
                    expr = ast.Compare(expressions[i], [ast.Lt()], [expressions[i+1]])
                    new_expressions.append(expr)

                case ast.LtE():
                    expr = ast.Compare(expressions[i], [ast.LtE()], [expressions[i+1]])
                    new_expressions.append(expr)

                case ast.Gt():
                    expr = ast.Compare(expressions[i], [ast.Gt()], [expressions[i+1]])
                    new_expressions.append(expr)

                case ast.GtE():
                    expr = ast.Compare(expressions[i], [ast.Lt()], [expressions[i+1]])
                    new_expressions.append(expr)

                case _:
                    # other operators are not support by Sympy
                    error = NotImplementedError(
                        f"Sympy does not support the {node.ops[i].__class__.__name__} operator, "
                        f"so the transformation is impossible."
                    )
                    raise error

        if len(new_expressions) == 1:
            # only one comparition
            return new_expressions[0]
        else:
            # transform into a And call
            return ast.Call(ast.Name('And'), new_expressions, [])


if __name__ == '__main__':

    code = 'a == b != c <= d'
    transformer = Transformer()
    tree = ast.parse(code)
    print(ast.dump(tree))
    new_tree = transformer.visit(tree)
    print(ast.dump(new_tree))
