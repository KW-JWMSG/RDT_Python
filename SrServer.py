from DataLayer import DataLayer
from UdpServer import UdpServer
import time
import random
import threading
import sys

class PacketLossError(Exception):
    def __init__(self):
        super().__init__('packet_loss')

    def __str__(self):
        return 'Packet Loss..'


class SrServer(threading.Thread):
    def __init__(self, winsize, delay_min, delay_max):
        threading.Thread.__init__(self)
        self.data = []
        self.buff_data = [None for i in range(winsize)]
        self.winsize = winsize
        self.min_sequence = 0
        self.max_sequence = self.min_sequence + winsize -1
        self.is_run = True

        self.server = UdpServer(self)
        self.server.start()
        self.delay_min = delay_min
        self.delay_max = delay_max

    def run(self):
        while self.is_run:
            if(self.buff_data[0] != None):
                if(self.buff_data[0].is_ack):
                    dataLayer = self.buff_data.pop(0)
                    self.data.append(dataLayer)
                    self.buff_data.append(None)
                    self.min_sequence+=1
                    self.max_sequence = self.min_sequence + self.winsize -1


    def deliver(self, dataLayer):
        delay_time = random.randint(self.delay_min, self.delay_max) / 1000
        if delay_time != 0:
            time.sleep(delay_time)
        #print(dataLayer.sequence, dataLayer.data)
        #print([i.sequence for i in self.data])
        #print(len(self.buff_data))
        if(dataLayer.sequence < self.min_sequence):
            return DataLayer(sequence=dataLayer.sequence, is_ack=True, is_err=False, is_dup=True, data="SERVER_RECEIVE_DUP")
        if(self.buff_data[0] != None):
            if(self.buff_data[0].sequence >= dataLayer.sequence):
                return DataLayer(sequence=dataLayer.sequence, is_ack=True, is_err=False, is_dup=True, data="SERVER_RECEIVE_DUP")
        if(dataLayer.sequence > self.max_sequence):
            return DataLayer(sequence=self.min_sequence, is_ack=True, is_err=True, data="SERVER_ERROR_OVR")
        if(dataLayer.is_err):
            return DataLayer(sequence=dataLayer.sequence, is_ack=True, is_err=True, data="SERVER_ERROR_LOS")
        if(dataLayer.is_end):
            self.is_run = False
            self.server.running = False
        ackLayer = DataLayer(sequence=dataLayer.sequence,
                             is_ack=True, is_err=False, data="SERVER_RECEIVE")
        dataLayer.is_ack = True
        self.buff_data[dataLayer.sequence - self.min_sequence] = dataLayer
        return ackLayer

    def recv(self, data):
        try:
            dataLayer = DataLayer(dumps=data)
            ackLayer = self.deliver(dataLayer)
            self.send(dataLayer=ackLayer)
        except PacketLossError:
            print(PacketLossError)
        except Exception as exception:
            print(exception)

    def send(self, dataLayer=DataLayer()):
        data = dataLayer.dumps()
        self.server.send(data)


if __name__ == '__main__':
    rs = SrServer(int(sys.argv[3]),int(sys.argv[1]),int(sys.argv[2]))
    rs.start()
