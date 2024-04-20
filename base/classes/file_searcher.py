import os


class FileSearch:
    def __is_python_file(self, path):
        return path.lower().endswith('.py')

    def __is_directory(self, path):
        return os.path.isdir(path)

    def __get_python_files(self, directory_path):
        python_files = []

        # Walk through the directory and its subdirectories recursively
        for root, dirs, files in os.walk(directory_path):
            # Check each file in the current directory
            for file in files:
                if file.endswith('.py'):  # Check if the file has a .py extension
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, directory_path)
                    python_files.append(relative_path)

        return python_files

    def get_files(self, path):
        if self.__is_python_file(path):
            return [path]
        elif self.__is_directory(path):
            return self.__get_python_files(path)
        else:
            return []
