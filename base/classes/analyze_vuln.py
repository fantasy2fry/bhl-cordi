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


class InsecureDeserializationDetector(ast.NodeVisitor):
    def __init__(self):
        self.analyzed_files = set()
        self.vulnerable_nodes = []
        self.description = []
        self.detailed_description = []

    def get_vulnerability_name(self):
        return ["Insecure Deserialization"]

    def visit_Call(self, node):
        # Check for dangerous functions like pickle.loads or yaml.load
        if isinstance(node.func, ast.Attribute):
            if (node.func.attr in ['loads', 'load'] and
                    isinstance(node.func.value, ast.Name) and
                    node.func.value.id in ['pickle', 'yaml', 'json']):
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

    def report_vulnerabilities(self, file_path):
        if self.vulnerable_nodes:
            self.description.append(
                f"Potential Insecure Deserialization vulnerabilities found in file: {file_path},")
            list_helper = []
            for node in self.vulnerable_nodes:
                list_helper.append(f"Line {node.lineno}: {ast.dump(node)}")
            self.detailed_description.append(list_helper)

    def display_vulnerabilities(self):
        for index, desc in enumerate(self.description):
            print(desc)
            for detail in self.detailed_description[index]:
                print(detail)

    def analyze_directory(self, directory_path):
        for root, dirs, files in os.walk(directory_path):
            for file_name in files:
                if file_name.endswith(".py"):
                    file_path = os.path.join(root, file_name)
                    print(f"Analyzing file: {file_path}")
                    self.analyze_file(file_path)
        self.display_vulnerabilities()


class CSRFDetector(ast.NodeVisitor):
    def __init__(self):
        self.analyzed_files = set()
        self.vulnerable_nodes = []
        self.description = []
        self.detailed_description = []

    def get_vulnerability_name(self):
        return ["Cross-Site Request Forgery (CSRF)"]

    def visit_FunctionDef(self, node):
        # Detecting potential CSRF in Flask or Django by checking if POST requests are handled without CSRF protection
        has_post_method = False
        has_csrf_protect = False

        for deco in node.decorator_list:
            if isinstance(deco, ast.Call):
                if isinstance(deco.func, ast.Attribute):
                    # Handle decorators like @app.route
                    if deco.func.attr == 'route':
                        # Check if the route decorator includes a method='POST'
                        for kw in deco.keywords:
                            if kw.arg == 'methods' and 'POST' in [m.s for m in kw.value.elts]:
                                has_post_method = True
                if 'csrf' in getattr(deco.func, 'id', '').lower() or 'csrf' in getattr(deco.func, 'attr', '').lower():
                    has_csrf_protect = True
            elif isinstance(deco, ast.Name):
                # Simple decorator names
                if 'csrf' in deco.id.lower():
                    has_csrf_protect = True

        if has_post_method and not has_csrf_protect:
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

    def report_vulnerabilities(self, file_path):
        if self.vulnerable_nodes:
            self.description.append(f"Potential CSRF vulnerabilities found in file: {file_path},")
            list_helper = []
            for node in self.vulnerable_nodes:
                list_helper.append(f"Line {node.lineno}: {ast.dump(node)}")
            self.detailed_description.append(list_helper)

    def display_vulnerabilities(self):
        for index, desc in enumerate(self.description):
            print(desc)
            for detail in self.detailed_description[index]:
                print(detail)

    def analyze_directory(self, directory_path):
        for root, dirs, files in os.walk(directory_path):
            for file_name in files:
                if file_name.endswith(".py"):
                    file_path = os.path.join(root, file_name)
                    print(f"Analyzing file: {file_path}")
                    self.analyze_file(file_path)
        self.display_vulnerabilities()


if __name__ == "__main__":
    directory_path = '../../additional'
    #
    #     # sql_detector = SQLInjectionDetector()
    # xss_detector = XSSDetector()
    #     path_traversal_detector = PathTraversalDetector()
    #
    #     # sql_detector.analyze_directory(directory_path)
    # xss_detector.analyze_directory(directory_path)
    #
    # insecure_deserialization = InsecureDeserializationDetector()

    # insecure_deserialization.analyze_directory(directory_path)

    csrf = CSRFDetector()
    csrf.analyze_directory(directory_path)

#     path_traversal_detector.analyze_directory(directory_path)
#
#     # print(xss_detector.description)
#     # print(xss_detector.detailed_description)
#
#     # sql_detector.display_vulnerabilities()
#     # xss_detector.display_vulnerabilities()
#
#     path_traversal_detector.display_vulnerabilities()
