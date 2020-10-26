import threading

class SrpServer(threading.Thread):
    def __init__(self, rdtCtrol, windows_size):
        threading.Thread.__init__(self)
        self.rdtCtrol = rdtCtrol 
        self.windows_size = windows_size

        self.cur_sequence = 0
        self.begin_sequence = 0
        self.end_sequence = (self.begin_sequence + windows_size) - 1

    def run(self):
        while self.rdtCtrol.isRunning():
            self.poolCheck()

    def sequenceCheck(self,sequence):
        if sequence < self.begin_sequence:
            return False
        elif sequence > self.end_sequence:
            return False
        return True

    def delivered(self,struct):
        print(struct.getSequence(), struct.getOperate(), struct.getMessage(), self.begin_sequence, self.end_sequence, self.cur_sequence)
        if(not self.sequenceCheck(struct.getSequence())):
            return False
        if(struct.getOperate() == 'SYN'):
            new_ack = self.rdtCtrol.make(sequence = struct.getSequence() ,operate='ACK',  message="ACK_MESSAGE", is_acked = True, is_delivered=True)
            self.rdtCtrol.send(new_ack)
            struct.setAcked(True)
            
            
        elif(struct.getOperate() == 'FIN'):
            new_ack = self.rdtCtrol.make(sequence = struct.getSequence() ,operate='ACK',  message="FIN_ACK", is_acked = True, is_delivered=True)
            self.rdtCtrol.send(new_ack)
            struct.setAcked(True)
            self.rdtCtrol.isRunning(False)
        
        self.rdtCtrol.recv_push(struct)
                       
    def poolCheck(self):
        f_struct = self.rdtCtrol.recv_get(0)
        if(f_struct == False):
            return False
        if f_struct.isAcked():
            p_struct = self.rdtCtrol.recv_pop(0)
            self.rdtCtrol.buff_push(p_struct)
            self.begin_sequence += 1
            self.end_sequence = (self.begin_sequence + self.windows_size) - 1
            self.cur_sequence += 1
