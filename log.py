class Log: 
    def __init__(self, filename):
        self.filename = filename

    def write(self, message):
        with open(self.filename, 'a') as f:
            f.write(message + '\n')
    def read(self):
        with open(self.filename, 'r') as f:
            return f.read()