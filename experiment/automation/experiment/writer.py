class Writer:
    def __init__(self, filename):
        self.filepath = "./data/{}".format(filename)

    def write(self, values):
        with open(self.filepath, 'a') as file:
            file.write('{}\n'.format(";".join(values)))
