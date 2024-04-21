import ast
import os


class Vulnerabilities:
    vulnerability_name = []
    vulnerability_description = []


class SQLInjectionDetector(ast.NodeVisitor):
    def __init__(self):
        self.analyzed_files = set()
        self.vulnerable_nodes = []
        self.description = []
        self.detailed_description = []

    def get_vulnerability_name(self):
        return ["SQL Injection"]

    def visit_BinOp(self, node):
        if isinstance(node.op, ast.Add):
            if (isinstance(node.left, ast.Str) or isinstance(node.left, ast.Name) or
                    isinstance(node.right, ast.Str) or isinstance(node.right, ast.Name)):
                self.vulnerable_nodes.append(node)
        self.generic_visit(node)

    def analyze_file(self, file_path):
        if file_path in self.analyzed_files:
            return

        self.analyzed_files.add(file_path)

        with open(file_path, 'r') as file:
            try:
                source_code = file.read()
                tree = ast.parse(source_code)
                self.visit(tree)
            except Exception as e:
                print(f"An error occurred while analyzing the file: {e}")

        self.report_vulnerabilities(file_path)

    def analyze_directory(self, directory_path):
        for root, dirs, files in os.walk(directory_path):
            for file_name in files:
                if file_name.endswith(".py"):
                    file_path = os.path.join(root, file_name)
                    print(f"Analyzing file: {file_path}")
                    self.analyze_file(file_path)
        self.display_vulnerabilities()

    def report_vulnerabilities(self, file_path):
        if self.vulnerable_nodes:
            self.description.append(f"Potential SQL Injection vulnerabilities found in file: {file_path},")
            list_helper = []
            for node in self.vulnerable_nodes:
                list_helper.append(f"Line {node.lineno}: {ast.dump(node)}")
            self.detailed_description.append(list_helper)

    def display_vulnerabilities(self):
        for index, desc in enumerate(self.description):
            print(desc)
            for detail in self.detailed_description[index]:
                print(detail)


class XSSDetector(ast.NodeVisitor):
    def __init__(self):
        self.analyzed_files = set()
        self.vulnerable_nodes = []
        self.description = []
        self.detailed_description = []

    def get_vulnerability_name(self):
        return ["Cross-Site Scripting (XSS)"]

    def visit_Str(self, node):
        if "'" in node.s or '"' in node.s:
            self.vulnerable_nodes.append(node)
        self.generic_visit(node)

    def analyze_file(self, file_path):
        if file_path in self.analyzed_files:
            return

        self.analyzed_files.add(file_path)

        with open(file_path, 'r') as file:
            try:
                source_code = file.read()
                tree = ast.parse(source_code)
                self.visit(tree)
            except Exception as e:
                print(f"An error occurred while analyzing the file: {e}")

        self.report_vulnerabilities(file_path)

    def analyze_directory(self, directory_path):
        for root, dirs, files in os.walk(directory_path):
            for file_name in files:
                if file_name.endswith(".py"):
                    file_path = os.path.join(root, file_name)
                    print(f"Analyzing file: {file_path}")
                    self.analyze_file(file_path)
        self.display_vulnerabilities()

    def report_vulnerabilities(self, file_path):
        if self.vulnerable_nodes:
            self.description.append(
                [f"Potential Cross-Site Scripting (XSS) vulnerabilities found in file: {file_path},"])
            list_helper = []
            for node in self.vulnerable_nodes:
                list_helper.append(f"Line {node.lineno}: {ast.dump(node)}")
            self.detailed_description.append(list_helper)

    def display_vulnerabilities(self):
        for index, desc in enumerate(self.description):
            print(desc)
            for detail in self.detailed_description[index]:
                print(detail)


if __name__ == "__main__":
    directory_path = '../../additional'

    #sql_detector = SQLInjectionDetector()
    xss_detector = XSSDetector()

    #sql_detector.analyze_directory(directory_path)
    xss_detector.analyze_directory(directory_path)

    print(xss_detector.description)
    print(xss_detector.detailed_description)

    #sql_detector.display_vulnerabilities()
    #xss_detector.display_vulnerabilities()
