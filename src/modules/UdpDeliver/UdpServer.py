import socket
import threading

_RTT = 60000 #Milli Second
_DEFAULT_TIMEOUT_SEC = _RTT / 1000   #Second

class UdpServer(threading.Thread):
    def __init__(self, bind, port, rdtCtrol, timeout = _DEFAULT_TIMEOUT_SEC):
        threading.Thread.__init__(self)
        self.bind = bind
        self.port = port 
        self.rdtCtrol = rdtCtrol
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(timeout)
        self.sock.bind((bind, port))
        print("open bind [", self.bind+":"+str(self.port),"]")
    

    def run(self):
        while self.recv():
            if(not self.rdtCtrol.isRunning()):
                break


    def recv(self):
        try:
            data, addr = self.sock.recvfrom(1024)
            self.addr = addr
            self.rdtCtrol.recv(data)
        except socket.timeout:
            print("TIME_OUT!", "접속된 클라이언트가 없어, 연결을 종료합니다.")
            self.rdtCtrol.isRunning(False)
            return False
        return True
    
    def send(self,send_data = None):
        snd_data = send_data or self.data
        self.sock.sendto(snd_data, self.addr)
