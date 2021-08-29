class decoder:
    """docstring for decoder."""
    def __init__(self, cb, var):
        self.callback = cb
        self.var = var
    while True:
        with open('test.json') as f:
            c = f.read()
        if c == 'callback':
            self.callback(1,'str2')
        else:
            self.callback('st1','str2')
        time.sleep(1)
