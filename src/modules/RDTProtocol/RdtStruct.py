import pickle
class RdtStruct:
    def __init__(self, sequence = -1, operate='SYN',  message='', is_delivered=False, is_error = False, is_acked=False, dumps=None):
        self.sequence = sequence
        self.operate  = operate
        self.message  = message
        self.is_delivered = is_delivered
        self.is_error = is_error
        self.is_acked = is_acked
        if(dumps != None):
            self.toObject(dumps)
    
    def getSequence(self):
        return self.sequence
    def getOperate(self):
        return self.operate
    def getMessage(self):
        return self.message
    def isDelivered(self):
        return self.is_delivered
    def isError(self):
        return self.is_error
    def isAcked(self):
        return self.is_acked
    def setDelivered(self,status):
        self.is_delivered = status
    def setError(self,status):
        self.is_error = statuss
    def setAcked(self,status):
        self.is_acked = status
    
    def toSerialize(self):
        return pickle.dumps(self)

    def toObject(self,dumps):
        obj = pickle.loads(dumps)
        self.sequence = obj.sequence
        self.operate  = obj.operate
        self.message  = obj.message
        self.is_delivered = obj.is_delivered
        self.is_error = obj.is_error
        self.is_acked = obj.is_acked