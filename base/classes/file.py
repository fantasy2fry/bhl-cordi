import astconverter as astc


class File:
    def __init__(self, file_path):
        self.converter = None
        self.file_path = file_path
        self.if_parsed = False
        self.content = None

    def parse(self):
        if not self.if_parsed:
            self.converter = astc.PythonASTConverter(self.file_path)
            self.content = self.converter.convert_to_ast()
            self.if_parsed = True

    def analyze_oop(self):
        pass

    def analyze_vuln(self):
        pass
