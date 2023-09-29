class Reader:
    def __init__(self, filename, filepath='./data/{}'):
        self.filepath = filepath.format(filename)

    def read(self):
        values = []

        with open(self.filepath, 'r') as file:
            for line in file.readlines():
                values.append(line.strip().split(";"))

        return values
