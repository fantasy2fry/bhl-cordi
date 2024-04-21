import ast
import os

from counter_mistakes import CounterMistakes


# tab_topic = []
# tab_file_name = []
# tab_description = []
# tab_solution = []


class HermetyzacjaVisitor(ast.NodeVisitor):
    """Klasa odwiedzająca węzły AST i sprawdzająca hermetyzację zmiennych klasowych."""

    tab_helper = []

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
        self.class_methods = {}
        self.abstract_classes = {}

    def visit_ImportFrom(self, node):
        for alias in node.names:
            self.imports[alias.name] = node.module

    def visit_ClassDef(self, node):
        bases = [base.id for base in node.bases if isinstance(base, ast.Name)]
        abstract_methods = []
        is_abstract = False

        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                for decorator in item.decorator_list:
                    if isinstance(decorator, ast.Name) and decorator.id == 'abstractmethod':
                        abstract_methods.append(item.name)
                        is_abstract = True

        self.classes[node.name] = {
            "file": self.current_file,
            "base_classes": bases,
            "methods": [item.name for item in node.body if isinstance(item, ast.FunctionDef)],
            "abstract_methods": abstract_methods,
            "is_abstract": is_abstract,
            "uses_super": False
        }

        if is_abstract:
            self.abstract_classes[node.name] = self.classes[node.name]

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

    def analyze_directory(self, directory, tab_topic, tab_file_name, tab_description, tab_solution):
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.py'):
                    self.current_file = os.path.join(root, file)

                    tab_file_name.append(str(file))

                    with open(self.current_file, 'r', encoding='utf-8') as file:
                        content = file.read()
                        tree = ast.parse(content)
                        self.visit(tree)

        self.check_diamond_inheritance(tab_topic, tab_file_name, tab_description, tab_solution)
        self.report_super_usage(tab_topic, tab_file_name, tab_description, tab_solution)
        self.check_polymorphism(tab_topic, tab_file_name, tab_description, tab_solution)
        self.check_static_variables(tab_topic, tab_file_name, tab_description, tab_solution)
        self.check_complex_inheritance(tab_topic, tab_file_name, tab_description, tab_solution)
        self.check_abstract_implementations(tab_topic, tab_file_name, tab_description,
                                            tab_solution)  # Upewnij się, że ta linia istnieje

        for topic, description in zip(tab_topic, tab_description):
            print(f"{topic}: {description}")

    def check_abstract_implementations(self, tab_topic, tab_file_name, tab_description, tab_solution):
        for class_name, class_info in self.classes.items():
            if not class_info['is_abstract']:
                for base in class_info['base_classes']:
                    if base in self.abstract_classes:
                        missing_methods = [method for method in self.abstract_classes[base]['abstract_methods'] if
                                           method not in class_info['methods']]
                        if missing_methods:
                            tab_topic.append("Missing abstract method implementations")
                            tab_description.append(
                                f"Class '{class_name}' does not implement all abstract methods from its base class '{base}'. Missing methods: {', '.join(missing_methods)}")

    def check_diamond_inheritance(self, tab_topic, tab_file_name, tab_description, tab_solution):
        for base_class, derived_classes in self.inheritance_tree.items():
            if len(derived_classes) > 1:
                common_bases = set()
                for derived in derived_classes:
                    common_bases.update(self.classes[derived]["base_classes"])
                if base_class in common_bases:
                    tab_topic.append("Diamond inheritance problem")
                    tab_description.append(
                        f"{base_class} is a common base class for {derived_classes}")

                    # print(f"Diamond inheritance detected: {base_class} is a common base class for {derived_classes}")

    def report_super_usage(self, tab_topic, tab_file_name, tab_description, tab_solution):
        for class_name, class_info in self.classes.items():
            if not class_info["uses_super"] and class_info["base_classes"]:
                tab_topic.append("Not using the super() function")
                tab_description.append(
                    f"The {class_name} class inherits from {class_info['base_classes']} and does not use super() in the constructor.")

                # print(
                #     f"The {class_name} class inherits from {class_info['base_classes']} and does not use super() in the constructor.")

    def check_polymorphism(self, tab_topic, tab_file_name, tab_description, tab_solution):
        for class_name, class_info in self.classes.items():
            base_classes = class_info["base_classes"]
            for base in base_classes:
                if base in self.class_methods:
                    base_methods = self.class_methods[base]
                    derived_methods = self.class_methods[class_name]
                    for method in base_methods:
                        if method not in derived_methods:
                            tab_topic.append("Problem with the polymorphism")
                            tab_description.append(
                                f"The {class_name} class does not override the '{method}' method of the {base} base class")

                            # print(f"Klasa {class_name} nie przesłania metody '{method}' z klasy bazowej {base}")

    def visit_Assign(self, node):
        # Jeśli obecnie przetwarzana jest klasa i przypisanie odbywa się poza funkcją (czyli na poziomie klasy)
        if isinstance(node.targets[0], ast.Name) and self.current_class:
            # Jeśli zmienna klasy (statyczna) została przypisana
            var_name = node.targets[0].id
            if "class_vars" not in self.classes[self.current_class]:
                self.classes[self.current_class]["class_vars"] = set()
            self.classes[self.current_class]["class_vars"].add(var_name)
        self.generic_visit(node)

    def check_static_variables(self, tab_topic, tab_file_name, tab_description, tab_solution):
        for class_name, class_info in self.classes.items():
            if "class_vars" in class_info:
                for var in class_info["class_vars"]:
                    tab_topic.append(f"Static variable issue")
                    tab_description.append(
                        f"Class '{class_name}' defines a static variable '{var}', which may cause side effects if modified across instances.")
        # Jeśli potrzebujesz, wyświetl zgromadzone informacje
        # for topic, description in zip(tab_topic, tab_description):
        #     print(f"{topic}: {description}")

    def check_complex_inheritance(self, tab_topic, tab_file_name, tab_description, tab_solution):
        for class_name, class_info in self.classes.items():
            base_classes = class_info["base_classes"]
            inheritance_depth = self.get_inheritance_depth(class_name, base_classes,
                                                           1)  # Start z 1, ponieważ klasa już istnieje
            if inheritance_depth > 2:  # Maksymalna dozwolona głębokość
                tab_topic.append("Complex inheritance hierarchy")
                tab_description.append(
                    f"Class '{class_name}' has a complex inheritance hierarchy with depth of {inheritance_depth}, which may complicate the codebase.")

    def get_inheritance_depth(self, class_name, base_classes, current_depth):
        if not base_classes:
            return current_depth
        max_depth = current_depth
        for base in base_classes:
            if base in self.classes and base in self.inheritance_tree:  # Upewnij się, że klasa bazowa jest znana i zarejestrowana
                new_depth = self.get_inheritance_depth(base, self.classes[base]["base_classes"], current_depth + 1)
                max_depth = max(max_depth, new_depth)
        return max_depth


class BasicAnalyserOOP:
    def __init__(self, directory_path, user_id):
        self.directory_path = directory_path
        self.tab_topic = []
        self.tab_file_name = []
        self.tab_description = []
        self.tab_solution = []
        self.user_id = user_id

        mapper = DependencyMapper()
        mapper.analyze_directory(directory_path, self.tab_topic, self.tab_file_name, self.tab_description,
                                 self.tab_solution)

        new_counter = CounterMistakes(self.user_id)
        new_counter.count_mistakes(self.tab_topic, self.tab_file_name, self.tab_description)
        dict_mistakes, file_count = new_counter.return_info()

        new_counter.calculate_tan()
        new_counter.write_to_csv()


if __name__ == "__main__":
    basic_object = BasicAnalyserOOP('../../additional', 1)



    # mapper = DependencyMapper()
    # directory_path = '../../additional'  # zmień na ścieżkę do twojego folderu testowego
    # mapper.analyze_directory(directory_path)
    #
    # # print(tab_topic)
    # # from translator import Translator
    # # print(tab_file_name)
    # # print(tab_topic)
    # # print(tab_description)
    # new_counter = CounterMistakes(1)
    # new_counter.count_mistakes(tab_topic, tab_file_name, tab_description)
    # dict_mistakes, file_count = new_counter.return_info()
    #
    # new_counter.calculate_tan()
    # new_counter.write_to_csv()
    #
    # print(file_count)
    # print(dict_mistakes)
