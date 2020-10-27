import pickle

class DataLayer:
    def __init__(self, sequence = -1, is_ack = False, is_err = False, data=None, dumps = None):
        self.sequence = sequence
        self.is_ack = is_ack
        self.is_err = is_err
        self.data = data
        if(dumps):
            self.loads(dumps)

    def dumps(self):
        return pickle.dumps(self)

    def loads(self, dumps):
        obj = pickle.loads(dumps)
        self.sequence = obj.sequence
        self.is_ack = obj.is_ack
        self.is_err = obj.is_err
        self.data = obj.data
        return self 