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


class GbnClient():
    def __init__(self, winsize, max_interval=12, min_interval=8, limit_cnt = 100, lossrate=1000):
        self.startTime =  time.time()
        self.limit_cnt = limit_cnt
        self.data = []
        self.buff_data = []
        self.winsize = winsize
        self.min_sequence = 0
        self.max_sequence = self.min_sequence + winsize - 1
        self.is_run = True

        self.current_sequence = 0
        self.client = UdpClient(self)
        self.max_interval = max_interval
        self.min_interval = min_interval
        self.timeout_cnt = 0
        self.packetloss_cnt = 0
        self.packetdup_cnt = 0
        self.sended_cnt = 0
        self.lossrate = lossrate

    def deliver(self, dataLayer,buff_idx):
        if(dataLayer.is_err):
            raise PacketLossError
        if(dataLayer.is_ack):
            if(self.buff_data[buff_idx].sequence == dataLayer.sequence):
                self.buff_data[buff_idx].is_ack = True
                if(buff_idx == 0):
                    data = self.buff_data.pop(0)
                    self.data.append(data)
        if(dataLayer.is_dup):
            self.packetdup_cnt += 1

    def recv(self,buff_idx):
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            try:
                interval = random.randint(self.min_interval, self.max_interval) / 1000
                future = executor.submit(self.client.recv)
                data = future.result(timeout=interval)
                dataLayer = DataLayer(dumps=data)
                self.deliver(dataLayer,buff_idx)
            except concurrent.futures.TimeoutError:
                #print('TimeOUT',self.timeout_cnt+1)
                self.timeout_cnt += 1
            except PacketLossError:
                #print('PacketLoss',self.packetloss_cnt+1)
                self.packetloss_cnt += 1
            
    def resend(self):
        for dt in self.buff_data:
            buff_idx = self.buff_data.index(dt)
            if(buff_idx == 0 and dt.is_ack):
                data = self.buff_data.pop(0)
                self.data.append(data)
                continue
            is_error = ((self.sended_cnt % self.lossrate +1 ) == 0)
            dt.is_err = is_error
            data = dt.dumps()
            self.client.send(data)
            self.recv(buff_idx)
            self.sended_cnt += 1

    def send(self,message='msg', is_end=False):
        while ((len(self.buff_data)>=self.winsize) and self.is_run):
            if(time.time()-self.startTime > self.limit_cnt):
                break
            self.resend()
        is_error = ((self.sended_cnt % self.lossrate) == 0)
        dataLayer = DataLayer(sequence = self.current_sequence, is_ack = False, is_err = is_error, is_end=is_end,  data=message)
        self.buff_data.append(dataLayer)
        data = dataLayer.dumps()
        self.client.send(data)
        buff_idx = self.buff_data.index(dataLayer)
        self.recv(buff_idx)
        self.current_sequence += 1
        self.sended_cnt += 1
        return True

    def stop(self):
        self.is_run = False

if __name__=='__main__':
    winsize = 50
    limit_cnt = 10
    max_interval = 10
    min_interval = 10

    startTime =  time.time()
    gc = GbnClient(winsize=winsize,limit_cnt=limit_cnt,max_interval=max_interval,min_interval=min_interval)
    pki = 0
    while (time.time()-startTime) <= limit_cnt:
        messages = 'message-'+str(pki)
        gc.send(message=messages)
        pki += 1
    gc.send(message='end',is_end=True)
    gc.stop()
    
    endTime = time.time()
    print("---------------PERFORMENCE---------------")
    print('START TIME\t:',startTime)
    print('END TIME\t:',endTime,'(GAP:',endTime-startTime,')')
    print('LAST SEQUENCE\t:',gc.current_sequence -1)
    print('LOSS\t\t:',gc.packetloss_cnt)
    print('TIMEOUT\t\t:',gc.timeout_cnt)
    print('DUP\t\t:',gc.packetdup_cnt)
    print('SEND\t\t:',gc.sended_cnt)
    print('SUCCESS\t:',len(gc.data))
    print("-----------------------------------------")
    
    


