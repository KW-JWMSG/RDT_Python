from DataLayer import DataLayer
from UdpClient import UdpClient
import concurrent.futures


class PacketLossError(Exception):
    def __init__(self):
        super().__init__('packet_loss')

    def __str__(self):
        return 'Packet Loss..'


class RdtClient:
    def __init__(self, interval, lossrate=1000):
        self.current_sequence = 0
        self.client = UdpClient(self)
        self.interval = interval / 1000
        self.timeout_cnt = 0
        self.packetloss_cnt = 0
        self.packetdup_cnt = 0
        self.sended_cnt = 0
        self.lossrate = lossrate

    def deliver(self, dataLayer):
        if(dataLayer.is_err):
            raise PacketLossError
        if(dataLayer.is_ack):
            self.current_sequence += 1
        if(dataLayer.is_dup):
            self.packetdup_cnt += 1

    def recv(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(self.client.recv)
            data = future.result(timeout=self.interval)
            dataLayer = DataLayer(dumps=data)
            self.deliver(dataLayer)
        
    def send(self,message='msg', is_end=False):
        while True:
            try:
                is_error = ((self.sended_cnt % self.lossrate) == 0)
                dataLayer = DataLayer(sequence = self.current_sequence, is_ack = False, is_err = is_error, is_end=False,  data=message)
                data = dataLayer.dumps()
                self.client.send(data)
                self.sended_cnt += 1
                self.recv()
                break
            except concurrent.futures.TimeoutError:
                print('TimeOUT',self.timeout_cnt+1)
                self.timeout_cnt += 1
            except PacketLossError:
                print('PacketLoss',self.packetloss_cnt+1)
                self.packetloss_cnt += 1


if __name__=='__main__':
    
    messages = ['message-'+str(i) for i in range(10000)]
    rc = RdtClient(1)
    for m in messages:
        rc.send(message=m)
    rc.send(message='end',is_end=True)

    print("---------------PERFORMENCE---------------")
    print('LAST SEQUENCE\t:',rc.current_sequence -1)
    print('LOSS\t\t:',rc.packetloss_cnt)
    print('TIMEOUT\t\t:',rc.timeout_cnt)
    print('DUP\t\t:',rc.packetdup_cnt)
    print('SEND\t\t:',rc.sended_cnt)
    print("-----------------------------------------")
    
    
