import socket
import threading

_RTT = 10 #Milli Second
_DEFAULT_TIMEOUT_SEC = _RTT / 1000   #Second

class UdpClient(threading.Thread):
    def __init__(self, bind, port, data, rdtCtrol, timeout = _DEFAULT_TIMEOUT_SEC, max_retry = 10):
        threading.Thread.__init__(self)
        self.bind = bind
        self.port = port 
        self.data = data
        self.rdtCtrol = rdtCtrol
        self.max_retry = max_retry
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(timeout)
    

    def run(self):
        if self.send():
            MAX_RETRY = self.max_retry
            while not self.recv() and MAX_RETRY > 0:
                if(not self.rdtCtrol.isRunning()):
                    break
                MAX_RETRY -= 1
                if(MAX_RETRY<=0):
                    self.rdtCtrol.isRunning(False)
                pass
        self.close()

    def close(self):
        self.sock.close()


    def send(self):
        self.sock.sendto(self.data, (self.bind, self.port))
        return True
          
    def recv(self):
        try:
            data, addr = self.sock.recvfrom(1024)
            self.rdtCtrol.recv(data)
        except ConnectionResetError:
            print("CONNECTION_ERROR", "SERVER 가 켜져있지 않거나, 인터넷 통신에 문제가 존재합니다.")
            self.close(self)
            self.rdtCtrol.isRunning(False)

            return False
        except socket.timeout:
            print("TIME_OUT!", "다시 수신 받습니다.")
            return False
        return True
            
