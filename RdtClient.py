from DataLayer import DataLayer
from UdpClient import UdpClient
import concurrent.futures
import random
import time
import sys


class PacketLossError(Exception):
    def __init__(self):
        super().__init__('packet_loss')

    def __str__(self):
        return 'Packet Loss..'


class RdtClient:
    def __init__(self,  max_interval=12, min_interval=8, lossrate=1000, limit_cnt=100):
        self.data = []
        self.current_sequence = 0
        self.client = UdpClient(self)
        self.max_interval = max_interval
        self.min_interval = min_interval
        self.timeout_cnt = 0
        self.packetloss_cnt = 0
        self.packetdup_cnt = 0
        self.sended_cnt = 0
        self.lossrate = lossrate
        self.startTime = time.time()

    def deliver(self, dataLayer):
        #print(dataLayer.sequence, dataLayer.data)
        if(dataLayer.is_err):
            raise PacketLossError
        if(dataLayer.is_dup):
            self.packetdup_cnt += 1
        if(dataLayer.is_ack):
            self.current_sequence += 1
            self.data.append(dataLayer)
            return True

    def recv(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            try:
                interval = random.randint(self.min_interval, self.max_interval) / 1000
                future = executor.submit(self.client.recv)
                data = future.result(timeout=interval)
                dataLayer = DataLayer(dumps=data)
                self.deliver(dataLayer)
                return True
            except concurrent.futures.TimeoutError:
                #print('TimeOUT', self.timeout_cnt+1)
                self.timeout_cnt += 1
                return False
            except PacketLossError:
                #print('PacketLoss', self.packetloss_cnt+1)
                self.packetloss_cnt += 1
                return False

    def send(self, message='msg', is_end=False):
        while True:
            if(time.time() - self.startTime > limit_cnt):
                break
            is_error = ((self.sended_cnt % self.lossrate) == 0)
            dataLayer = DataLayer(sequence=self.current_sequence,
                                  is_ack=False, is_err=is_error, is_end=False,  data=message)
            data = dataLayer.dumps()
            self.client.send(data)
            self.sended_cnt += 1
            if self.recv():
                break


if __name__ == '__main__':
    limit_cnt = 100
    max_interval =10
    min_interval = 10

    startTime = time.time()
    rc = RdtClient(max_interval=max_interval,min_interval=min_interval)
    pki = 0
    while (time.time()-startTime) <= limit_cnt:
        messages = 'message-'+str(pki)
        rc.send(message=messages)
        pki += 1
    rc.send(message='end', is_end=True)
    endTime = time.time()
    print("---------------PERFORMENCE---------------")
    print('START TIME\t:', startTime)
    print('END TIME\t:', endTime, '(GAP:', endTime-startTime, ')')
    print('LAST SEQUENCE\t:', rc.current_sequence - 1)
    print('LOSS\t\t:', rc.packetloss_cnt)
    print('TIMEOUT\t\t:', rc.timeout_cnt)
    print('DUP\t\t:', rc.packetdup_cnt)
    print('SEND\t\t:', rc.sended_cnt)
    print('SUCCESS\t:', len(rc.data))
    print("-----------------------------------------")
