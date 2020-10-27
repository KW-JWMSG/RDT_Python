import socket

class UdpClient:
    def __init__(self,data_controller, data_layer, raw_data, host="127.0.0.1", port=5000):
        self.data_controller = data_controller
        self.data_layer = data_layer
        self.raw_data = raw_data

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(timeout)
        self.server_addr = (host, port)
        print("open bind [", host+":"+str(port),"]")
    
    def close(self):
        self.sock.close()

    def recv(self):
        data, addr = self.sock.recvfrom(1024)
        self.data_controller.recv(data)

    def send(self):
        self.sock.sendto(raw_data, self.server_addr)    