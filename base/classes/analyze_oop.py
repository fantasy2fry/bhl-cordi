import ast
import os


class HermetyzacjaVisitor(ast.NodeVisitor):
    """Klasa odwiedzająca węzły AST i sprawdzająca hermetyzację zmiennych klasowych."""

    def visit_ClassDef(self, node):
        print(f"Analiza klasy {node.name}:")
        has_private = False
        has_public = False

        for body_item in node.body:
            if isinstance(body_item, ast.FunctionDef) and body_item.name == '__init__':
                for stmt in body_item.body:
                    if isinstance(stmt, ast.Assign):
                        for target in stmt.targets:
                            if isinstance(target, ast.Attribute) and isinstance(target.value,
                                                                                ast.Name) and target.value.id == 'self':
                                if target.attr.startswith('_'):
                                    has_private = True
                                else:
                                    has_public = True
                                print(
                                    f"  {'Prywatna' if target.attr.startswith('_') else 'Publiczna'} zmienna: {target.attr}")

        if has_public:
            print(
                f"  Uwaga: W klasie {node.name} zdefiniowano publiczne zmienne. Zalecana jest hermetyzacja poprzez użycie podkreślnika.")
        if not has_private:
            print(f"  Brak prywatnych zmiennych w klasie {node.name}. Zalecane jest ich zdefiniowanie.")

        self.generic_visit(node)


class DependencyMapper(ast.NodeVisitor):
    def __init__(self):
        self.imports = {}
        self.classes = {}
        self.current_class = None
        self.inheritance_tree = {}

    def visit_ImportFrom(self, node):
        for alias in node.names:
            self.imports[alias.name] = node.module

    def visit_ClassDef(self, node):
        bases = [base.id for base in node.bases if isinstance(base, ast.Name)]
        self.classes[node.name] = {
            "file": self.current_file,
            "base_classes": bases,
            "uses_super": False
        }
        for base in bases:
            if base in self.inheritance_tree:
                self.inheritance_tree[base].append(node.name)
            else:
                self.inheritance_tree[base] = [node.name]
        self.current_class = node.name
        self.generic_visit(node)
        self.current_class = None

    def visit_FunctionDef(self, node):
        if self.current_class and node.name == "__init__":
            for stmt in ast.walk(node):
                if isinstance(stmt, ast.Call) and isinstance(stmt.func, ast.Attribute):
                    if stmt.func.attr == "__init__" and isinstance(stmt.func.value,
                                                                   ast.Call) and stmt.func.value.func.id == "super":
                        self.classes[self.current_class]["uses_super"] = True
        self.generic_visit(node)

    def analyze_file(self, file_path):
        self.current_file = file_path
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            tree = ast.parse(content)
            self.visit(tree)

    def analyze_directory(self, directory):
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    print(f"Analiza pliku: {file_path}")
                    self.analyze_file(file_path)

        self.check_diamond_inheritance()
        self.report_super_usage()

    def check_diamond_inheritance(self):
        for base_class, derived_classes in self.inheritance_tree.items():
            if len(derived_classes) > 1:
                common_bases = set()
                for derived in derived_classes:
                    common_bases.update(self.classes[derived]["base_classes"])
                if base_class in common_bases:
                    print(f"Diamond inheritance detected: {base_class} is a common base class for {derived_classes}")

    def report_super_usage(self):
        for class_name, class_info in self.classes.items():
            if not class_info["uses_super"] and class_info["base_classes"]:
                print(
                    f"Klasa {class_name} dziedziczy po {class_info['base_classes']} i nie używa super() w konstruktorze.")


if __name__ == "__main__":
    mapper = DependencyMapper()
    directory_path = '../../additional'  # zmień na ścieżkę do twojego folderu testowego
    mapper.analyze_directory(directory_path)
