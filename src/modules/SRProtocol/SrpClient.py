import threading

class SrpClient(threading.Thread):
    def __init__(self, message_pool, rdtCtrol, windows_size):
        threading.Thread.__init__(self)
        self.message_pool = message_pool
        self.rdtCtrol = rdtCtrol 
        self.windows_size = windows_size

        self.cur_sequence = 0
        self.begin_sequence = 0
        self.end_sequence = (self.begin_sequence + windows_size) - 1

        self.genPool()

    def run(self):
        while self.rdtCtrol.isRunning():
            try:

                self.poolCheck()
                struct =  self.rdtCtrol.struct_pool.pop(0)
                if(struct == None):
                    continue
                while(not self.sequenceCheck(struct.getSequence())):
                    pass
                self.rdtCtrol.send_push(struct)
                self.rdtCtrol.send(struct)
            
            except IndexError:
                self.rdtCtrol.isRunning(False)
                continue
            
    def genPool(self):
        for message in self.message_pool:
            struct = self.rdtCtrol.make(operate='SYN',  message=message)
            self.rdtCtrol.pool_push(struct)
        fin_struct = self.rdtCtrol.make(operate='FIN',  message="FIN_MESSAGE")
        self.rdtCtrol.pool_push(fin_struct)

    def sequenceCheck(self,sequence):
        if sequence < self.begin_sequence:
            return False
        elif sequence > self.end_sequence:
            return False
        return True
    
    def delivered(self,struct):
        if(not self.sequenceCheck(struct.getSequence())):
            return False
        print(struct.getSequence(), struct.getOperate(), struct.getMessage(), self.begin_sequence, self.end_sequence, self.cur_sequence)
        delivered_struct = self.rdtCtrol.send_get(struct.getSequence() - self.begin_sequence)
        delivered_struct.setDelivered(True)

        if(struct.getOperate() == 'ACK'):
            delivered_struct.setAcked(True)
            
        if(struct.getOperate() == 'NCK'):
            self.rdtCtrol.send(delivered_struct)
                       
    def poolCheck(self):
        f_struct = self.rdtCtrol.send_get()
        if(f_struct == False):
            return False
        if f_struct.isAcked():
            p_struct = self.rdtCtrol.send_pop(0)
            self.rdtCtrol.buff_push(p_struct)
            self.begin_sequence += 1
            self.end_sequence = (self.begin_sequence + self.windows_size) - 1
            self.cur_sequence += 1
        #print(self.rdtCtrol.struct_buff)
