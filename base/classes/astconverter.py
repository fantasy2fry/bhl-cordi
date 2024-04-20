import ast


class PythonASTConverter:
    """Klasa do wczytywania plików Pythona i konwersji ich zawartości do drzewa AST."""

    def __init__(self, file_path):
        self.file_path = file_path

    def convert_to_ast(self):
        """Wczytaj plik i przekonwertuj jego zawartość na drzewo AST."""
        with open(self.file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            return ast.parse(content, filename=self.file_path)
