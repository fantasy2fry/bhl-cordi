

class Raport:
    def __init__(self, folder):
        self.folder = folder
        self.text = []

    def add_file_raport(self, file_path, tb1, tb2):
        self.text.append(f"Analiza pliku: {file_path}")
        self.text.append(f"  {tb1}")
        self.text.append(f"  {tb2}")
        self.text.append("")