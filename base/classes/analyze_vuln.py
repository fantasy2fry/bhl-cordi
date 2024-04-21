import ast
import os


class SQLInjectionDetector(ast.NodeVisitor):
    def __init__(self):
        self.vulnerable_nodes = []

    def visit_BinOp(self, node):
        if isinstance(node.op, ast.Add):
            if (isinstance(node.left, ast.Str) or isinstance(node.left, ast.Name) or
                    isinstance(node.right, ast.Str) or isinstance(node.right, ast.Name)):
                self.vulnerable_nodes.append(node)
        self.generic_visit(node)

    def analyze_file(self, file_path):
        with open(file_path, 'r') as file:
            try:
                source_code = file.read()
                tree = ast.parse(source_code)
                self.visit(tree)
            except Exception as e:
                print(f"An error occurred while analyzing the file: {e}")

    def report_vulnerabilities(self, file_path):
        if self.vulnerable_nodes:
            print(f"Potential SQL Injection vulnerabilities found in file: {file_path}")
            for node in self.vulnerable_nodes:
                print(f"Line {node.lineno}: {ast.dump(node)}")


if __name__ == "__main__":
    directory_path = '../../additional'

    detector = SQLInjectionDetector()

    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            if file_name.endswith(".py"):
                file_path = os.path.join(root, file_name)
                print(f"Analyzing file: {file_path}")
                detector.analyze_file(file_path)
                detector.report_vulnerabilities(file_path)
