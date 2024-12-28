from .ExpressionNode import ExpressionNode
from .StatementsNode import StatementsNode
from .BinaryOperatorNode import BinaryOperatorNode


class IfNode(ExpressionNode):
    """Класс узла операторов для  AST."""

    def __init__(
        self,
        then_node: StatementsNode,
        else_node: StatementsNode | None,
        condition_node: BinaryOperatorNode,
    ):
        self.then_node = then_node
        self.else_node = else_node
        self.condition_node = condition_node

    def __eq__(self, value):
        return (
            isinstance(value, IfNode)
            and self.then_node == value.then_node
            and self.condition_node == value.condition_node
        )

    def to_python(self, indent_level) -> str:
        indent = indent_level * " "
        python_code = indent + f"if {self.condition_node.to_python(indent_level=0)}:\n"

        if not self.then_node.code_strings_nodes:
            python_code += (" " * (indent_level + 4) + "pass")
        else:
            python_code += self.then_node.to_python(indent_level=indent_level + 4)

        if self.else_node:
            python_code += ('\n' + indent_level * " " + "else:\n")

            if not self.else_node.code_strings_nodes:
                python_code += (" " * (indent_level + 4) + "pass")

            python_code += self.else_node.to_python(indent_level=indent_level + 4)
        return python_code