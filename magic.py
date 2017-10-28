import os
import tempfile


class File:
    def __init__(self, filename):
        self.filename = os.path.abspath(filename)
        self.f = open(self.filename, "a")
        self.f.close()

    def write(self, string):
        with open(self.filename, "a") as f:
            f.write(string)

    def get_content(self):
        with open(self.filename, 'r') as f:
            return f.read()

    def __add__(self, two):
        with open(os.path.join(tempfile.gettempdir(), 'new_file.txt'), 'w') as new_file:
            new_file.write(self.get_content() + two.get_content())
        return File(os.path.join(tempfile.gettempdir(), 'new_file.txt'))


first = File('file1.txt')
second = File('file2.txt')
new_obj = first + second