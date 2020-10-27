import threading

class GbnServer(threading.Thread):
    def __init__(self, rdtCtrol):
        threading.Thread.__init__(self)
        self.rdtCtrol = rdtCtrol 

        self.cur_sequence = 0

    def run(self):
        while self.rdtCtrol.isRunning():
            self.poolCheck()

    def delivered(self,struct):
        print(struct.getSequence(), struct.getOperate(), struct.getMessage(), self.cur_sequence)
        if(struct.getSequence() != self.cur_sequence+1 ):
            new_ack = self.rdtCtrol.make(sequence = self.cur_sequence ,operate='ACK',  message="ACK_MESSAGE", is_acked = True, is_delivered=True)
            self.rdtCtrol.send(new_ack)
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
            self.cur_sequence += 1
        