import pickle

class DataLayer:
    def __init__(self, sequence = -1, is_ack = False, is_err = False, data=None, is_end = False, is_dup = False, dumps = None):
        self.sequence = sequence
        self.is_ack = is_ack
        self.is_err = is_err
        self.data = data
        self.is_end = is_end
        self.is_dup = is_dup
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
        self.is_end = obj.is_end
        self.is_dup = obj.is_dup
        return self 