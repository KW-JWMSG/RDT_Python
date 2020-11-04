import socket

class UdpClient:
    def __init__(self, data_controller, host="127.0.0.1", port=5000):
        self.data_controller = data_controller

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_addr = (host, port)
    
    def close(self):
        self.sock.close()

    def recv(self):
        data, addr = self.sock.recvfrom(1024)
        return data

    def send(self,raw_data):
        self.sock.sendto(raw_data, self.server_addr)    
