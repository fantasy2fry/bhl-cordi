import ast
import os


class PythonASTConverter:
    """Klasa do wczytywania plików Pythona i konwersji ich zawartości do drzewa AST."""

    def __init__(self, file_path):
        self.file_path = file_path

    def convert_to_ast(self):
        """Wczytaj plik i przekonwertuj jego zawartość na drzewo AST."""
        with open(self.file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            return ast.parse(content, filename=self.file_path)


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


def analyze_file(file_path):
    """Analizuj plik pod kątem zasad hermetyzacji zmiennych w klasach."""
    converter = PythonASTConverter(file_path)
    syntax_tree = converter.convert_to_ast()
    visitor = HermetyzacjaVisitor()
    visitor.visit(syntax_tree)


def analyze_directory(directory):
    """Przeszukaj folder w poszukiwaniu plików Pythona i analizuj każdy z nich."""
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                print(f"Analiza pliku: {file_path}")
                analyze_file(file_path)
                print("")  # Dla lepszego oddzielenia wyników


def analyze_path(path):
    if os.path.isdir(path):
        analyze_directory(path)
    elif os.path.isfile(path) and path.endswith('.py'):
        print(f"Analizuję plik: {path}")
        analyze_file(path)
    else:
        print("Podana ścieżka nie jest katalogiem ani plikiem .py")


# Przykład użycia:
path = 'tester_code.py'
analyze_path(path)
