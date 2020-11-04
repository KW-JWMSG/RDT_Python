from DataLayer import DataLayer
from UdpServer import UdpServer


class PacketLossError(Exception):
    def __init__(self):
        super().__init__('packet_loss')

    def __str__(self):
        return 'Packet Loss..'


class RdtServer:
    def __init__(self):
        self.data = []
        self.current_sequence = 0
        self.server = UdpServer(self)
        self.server.start()

    def deliver(self, dataLayer):
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
    rs = RdtServer()