import time
from matplotlib import pyplot as plt
from multiprocessing import Process
from RdtClient import RdtClient
from GbnClient import GbnClient
from SrClient import SrClient
from RdtServer import RdtServer
from GbnServer import GbnServer
from SrServer import SrServer




def rdt_perform_graph_client(max_interval, min_interval, limit_time, delay_min, delay_max):
    result = []
    loss_rate = 10
    for m in range(1,10):
        p = Process(target=RdtServer, args=(delay_min,delay_max,))
        p.start()
        time.sleep(2)
        print("RDT_RUN_",m)
        startTime = time.time()
        rc = RdtClient(max_interval=max_interval,min_interval=min_interval,lossrate=loss_rate**m)
        pki = 0
        while (time.time()-startTime) <= limit_time:
            messages = 'message-'+str(pki)
            rc.send(message=messages)
            pki += 1
        rc.send(message='end', is_end=True)
        endTime = time.time()
        result.append({"timming":m,"lossrate":loss_rate**m,"startTime":startTime, 'endTime':endTime, 'success':len(rc.data), 'dup':rc.packetdup_cnt, 'snd':rc.sended_cnt, 'perform':len(rc.data)/(endTime-startTime)})
        print({"timming":m,"lossrate":loss_rate**m,"startTime":startTime, 'endTime':endTime, 'success':len(rc.data), 'dup':rc.packetdup_cnt, 'snd':rc.sended_cnt,'perform':len(rc.data)/(endTime-startTime)})
        p.terminate()
    return result

def gbn_perform_graph_client(max_interval, min_interval, limit_time, s_windowsize, delay_min, delay_max, r_windowsize):
    result = []
    loss_rate = 10
    for m in range(1,10):
        p = Process(target=GbnServer, args=(r_windowsize,delay_min,delay_max,))
        p.start()
        time.sleep(2)
        print("GBN_RUN_",m)
        startTime = time.time()
        gc = GbnClient(s_windowsize,min_interval=min_interval, max_interval=max_interval,lossrate=loss_rate**m,limit_cnt=limit_time)
        pki = 0
        while (time.time()-startTime) <= limit_time:
            messages = 'message-'+str(pki)
            gc.send(message=messages)
            pki += 1
        gc.send(message='end', is_end=True)
        endTime = time.time()
        result.append({"timming":m,"lossrate":loss_rate**m,"startTime":startTime, 'endTime':endTime, 'success':len(gc.data), 'dup':gc.packetdup_cnt, 'snd':gc.sended_cnt,'perform':len(gc.data)/(endTime-startTime)})
        print({"timming":m,"lossrate":loss_rate**m,"startTime":startTime, 'endTime':endTime, 'success':len(gc.data), 'dup':gc.packetdup_cnt, 'snd':gc.sended_cnt,'perform':len(gc.data)/(endTime-startTime)})
        p.terminate()
    return result

def sr_perform_graph_client(max_interval, min_interval, limit_time, s_windowsize, delay_min, delay_max, r_windowsize):
    result = []
    loss_rate = 10
    for m in range(1,10):
        p = Process(target=SrServer, args=(r_windowsize,delay_min,delay_max,))
        p.start()
        time.sleep(2)
        print("SR_RUN_",m)
        startTime = time.time()
        gc = SrClient(s_windowsize,min_interval=min_interval, max_interval=max_interval,lossrate=loss_rate**m,limit_cnt=limit_time)
        pki = 0
        while (time.time()-startTime) <= limit_time:
            messages = 'message-'+str(pki)
            gc.send(message=messages)
            pki += 1
        gc.send(message='end', is_end=True)
        endTime = time.time()
        result.append({"timming":m,"lossrate":loss_rate**m,"startTime":startTime, 'endTime':endTime, 'success':len(gc.data), 'dup':gc.packetdup_cnt, 'snd':gc.sended_cnt,'perform':len(gc.data)/(endTime-startTime)})
        print({"timming":m,"lossrate":loss_rate**m,"startTime":startTime, 'endTime':endTime, 'success':len(gc.data), 'dup':gc.packetdup_cnt, 'snd':gc.sended_cnt,'perform':len(gc.data)/(endTime-startTime)})
        p.terminate()
    return result


if __name__ == '__main__':
    #result = rdt_perform_graph_client(10,10,100,8,12)
    #result = gbn_perform_graph_client(10,10,5,8,12,50)
    result = sr_perform_graph_client(10,10,100,10,8,12,10)
    plt_x = [str(1/r['lossrate']) for r in result]
    plt_y = [r['perform'] for r in result]
    plt.plot(plt_x, plt_y)
    plt.xlabel('loss rate')
    plt.ylabel('performence')
    plt.title('performenceCheck')
    plt.show()
