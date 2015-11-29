import string

class PathName(object):
    def __init__(self, name):
        self.name = name
    def absolute(self):
        return self.name.startswith('/')
    def __eq__(self, other):
        if self.name == other.name:
            return True
        if not self.absolute() and other.absolute():
            return other == self
        if self.absolute() and not other.absolute():
            filename = self.name.split('/')[-1]
            if not filename.startswith(other.name):
                return False
            if len(filename) < len(other.name):
                return False
            if len(filename) == len(other.name):
                return True
            if filename[len(other.name):len(other.name)+1] in string.ascii_letters:
                return False
            return True
        return False
    def __str__(self):
        return self.name
