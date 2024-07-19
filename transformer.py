import ast


class Transformer(ast.NodeTransformer):
    '''
    Node transformer used to convert `Python` logic syntax into `Sympy` logic syntax
    This class will only take a combination of the following nodes (ast.BoolOp, ast.BinOp,
    ast.UnaryOp, ast.Compare, ast.Call, ast.Constant, ast.Name); an error will be raised if
    any other node is encountered.
    '''

    def visit_BoolOp(self, node: ast.BoolOp) -> ast.Call:

        values = [self.visit(v) for v in node.values]

        match node.op:

            case ast.Or():
                return ast.Call(ast.Name('Or'), values)

            case ast.And():
                return ast.Call(ast.Name('And'), values)

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
            return ast.Call(ast.Name('Not'), [operand])
        else:
            return ast.UnaryOp(node.op, operand)


if __name__ == '__main__':

    code = '(not a and b) or c'
    transformer = Transformer()
    tree = ast.parse(code)
    new_tree = transformer.visit(tree)
    print(ast.dump(new_tree))
