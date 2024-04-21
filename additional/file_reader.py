import os


def read_file(file_name):
    with open(file_name, 'r') as file:
        return file.read()


if __name__ == "__main__":
    file_name = input("Enter the name of the file to read: ")
    file_path = os.path.join('./data/', file_name)

    if os.path.exists(file_path):
        content = read_file(file_path)
        print("File content:")
        print(content)
    else:
        print("File not found.")
