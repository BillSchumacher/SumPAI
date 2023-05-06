import ast
from typing import Dict

from loguru import logger


class CodeExtractor(ast.NodeVisitor):
    """Extracts Python classes and functions from the given source code.

    Attributes:
        functions (Dict[str, str]): A dictionary containing the function names
            and their corresponding source code.
        classes (Dict[str, dict]): A dictionary containing the class names and
            a dictionary with the class source code and the class functions.
    """

    def __init__(self) -> None:
        self.functions: Dict[str, str] = {}
        self.classes: Dict[str, Dict[str, Dict[str, str]]] = {}
        self.global_level_code = []

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Visits function definitions and saves their source code.

        Args:
            node (ast.FunctionDef): The function definition node.
        """
        logger.debug(f"Visiting function {node.name}")
        source_code = ast.unparse(node)
        function_name = node.name
        self.functions[function_name] = source_code

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Visits class definitions and saves their source code and functions.

        Args:
            node (ast.ClassDef): The class definition node.
        """
        logger.debug(f"Visiting class {node.name}")
        source_code = ast.unparse(node)
        class_name = str(node.name)
        class_functions = {
            str(child_node.name): ast.unparse(child_node)
            for child_node in ast.iter_child_nodes(node)
            if isinstance(child_node, ast.FunctionDef)
        }
        self.classes[class_name] = {  # type: ignore
            "source_code": source_code,
            "functions": class_functions,
        }

    def extract_global_level_code(self, tree: ast.AST):
        for node in ast.iter_child_nodes(tree):
            if not isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                self.global_level_code.append(ast.unparse(node))
