import socket
import threading

class UdpServer(threading.Thread):
    def __init__(self,data_controller, host="127.0.0.1", port=5000):
        super().__init__()
        self.data_controller = data_controller
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((host, port))
        self.sock.settimeout(10) #패킷이 10초간 안들어 올 경우 Timeout 후 종료
        self.running = True
        print("open bind [", host+":"+str(port),"]")
    
    def close(self):
        self.sock.close()

    def recv(self):
        data, addr = self.sock.recvfrom(1024)
        self.client_addr = addr
        self.data_controller.recv(data)

    def send(self,raw_data):
        if(self.client_addr == None):
            raise "아직 Listen 중인 서버가 아닙니다."
        self.sock.sendto(raw_data, self.client_addr)    

    def run(self):
        try:
            while self.running:
                self.recv()
        except socket.timeout:
            print("TIMEOUT_FINISH")
