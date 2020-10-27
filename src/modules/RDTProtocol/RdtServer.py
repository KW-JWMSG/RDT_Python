from ..UdpDeliver.UdpServer import UdpServer
from .RdtStruct import RdtStruct
from ..SRProtocol.SrpServer import SrpServer
from ..GBNProtocol.GbnServer import GbnServer

_RTT = 60000 #Milli Second
_DEFAULT_TIMEOUT_SEC = _RTT / 1000   #Second

class RdtServer:
    def __init__(self, server_host, server_port, windows_size, timeout = _DEFAULT_TIMEOUT_SEC, buffer_type="SR"):
        self.server_host = server_host
        self.server_port = server_port
        self.windows_size = windows_size
        self.buffer_type = buffer_type
        self.udp_server = UdpServer(server_host, server_port, self, timeout=timeout)
    
        self.struct_recv = []
        self.struct_buff = []
        self.is_running = True
        
        self.srpServer = SrpServer(self,windows_size)
        self.gbnServer = GbnServer(self)

        if(buffer_type == "SR"):
            self.deliveryServer = self.srpServer
        else:
            self.deliveryServer = self.gbnServer

        self.start()


    def start(self):
        self.udp_server.start()
        self.deliveryServer.start()


    def recv(self,data):
        recv_struct = RdtStruct(dumps=data)
        self.deliveryServer.delivered(recv_struct)

    def send(self,send_structure):
        send_data = send_structure.toSerialize()
        self.udp_server.send(send_data)

    def make(self,sequence = None, operate='SYN',  message='', is_delivered=False, is_error = False, is_acked=False):
        new_sequence = sequence
        if(new_sequence == None):
            new_sequence = len(self.struct_pool)
        new_struct = RdtStruct(sequence = new_sequence, operate=operate,  message=message, is_delivered=is_delivered, is_error = is_error, is_acked=is_acked)
        return new_struct

    def buff_push(self,struct):
        self.struct_buff.append(struct)

    def recv_push(self,struct):
        self.struct_recv.append(struct)
    def recv_pop(self,pos = 0):
        self.struct_recv.pop(pos)
    def recv_get(self,pos=0):
        try:
            return self.struct_recv[pos]
        except IndexError:
            return False

    def isRunning(self,status=None):
        if(status == None):
            return self.is_running
        self.is_running = status