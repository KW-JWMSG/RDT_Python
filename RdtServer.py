from DataLayer import DataLayer
from UdpServer import UdpServer
import time
import random
import sys


class PacketLossError(Exception):
    def __init__(self):
        super().__init__('packet_loss')

    def __str__(self):
        return 'Packet Loss..'


class RdtServer:
    def __init__(self,delay_min, delay_max):
        self.data = []
        self.current_sequence = 0
        self.server = UdpServer(self)
        self.server.start()
        self.delay_min = delay_min
        self.delay_max = delay_max

    def deliver(self, dataLayer):
        #print(dataLayer.sequence, dataLayer.data,self.current_sequence)
        delay_time = random.randint(self.delay_min,self.delay_max) / 1000
        if delay_time != 0:
            time.sleep(delay_time)
        if(dataLayer.is_err):
            return DataLayer(sequence=self.current_sequence, is_ack=True, is_err=True, data="SERVER_ERROR_LOS")
        if(dataLayer.is_end):
            self.server.running = False
            self.server.close()
        if(dataLayer.sequence > self.current_sequence):
            return DataLayer(sequence=self.current_sequence, is_ack=True, is_err=True, data="SERVER_ERROR_OVR")
        if(dataLayer.sequence < self.current_sequence):
            return DataLayer(sequence=self.current_sequence, is_ack=True, is_err=False, is_dup=True, data="SERVER_RECEIVE_DUP")    
        ackLayer = DataLayer(sequence=self.current_sequence,
                             is_ack=True, is_err=False, data="SERVER_RECEIVE")
        self.current_sequence += 1
        self.data.append(dataLayer)
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
    rs = RdtServer(int(sys.argv[1]),int(sys.argv[2]))
