from ..UdpDeliver.UdpClient import UdpClient
from .RdtStruct import RdtStruct
from ..SRProtocol.SrpClient import SrpClient
from ..GBNProtocol.GbnClient import GbnClient

_RTT = 60000 #Milli Second
_DEFAULT_TIMEOUT_SEC = _RTT / 1000   #Second

class RdtClient:
    def __init__(self, server_host, server_port, windows_size, message_pool, timeout = _DEFAULT_TIMEOUT_SEC, buffer_type="SR"):
        self.server_host = server_host
        self.server_port = server_port
        self.windows_size = windows_size
        self.timeout = timeout
        self.buffer_type = buffer_type
        self.udp_pool = []

        
        self.struct_pool = []
        self.struct_send = []
        self.struct_buff = []

        self.is_running = True

        self.srpClient = SrpClient(message_pool,self,windows_size)
        self.gbnClient = GbnClient(message_pool,self,windows_size)

        if(buffer_type == "SR"):
            self.deliveryClient = self.srpClient
        else:
            self.deliveryClient = self.gbnClient

        self.start()

    def start(self):
        self.deliveryClient.start()
        
    def recv(self,data):
        recv_struct = RdtStruct(dumps=data)
        self.deliveryClient.delivered(recv_struct)

    def send(self,send_struct):
        send_data = send_struct.toSerialize()
        udp_client = UdpClient(self.server_host, self.server_port, send_data, self, self.timeout)
        udp_client.run()
        self.udp_pool.append(udp_client)

    def make(self,sequence = None, operate='SYN',  message='', is_delivered=False, is_error = False, is_acked=False):
        new_sequence = sequence
        if(new_sequence == None):
            new_sequence = len(self.struct_pool)
        new_struct = RdtStruct(sequence = new_sequence, operate=operate,  message=message, is_delivered=is_delivered, is_error = is_error, is_acked=is_acked)
        return new_struct

    def pool_push(self, struct):
        self.struct_pool.append(struct)
    def pool_pop(self,pos = 0):
        try:
            self.struct_pool.pop(pos)
        except IndexError:
            return None
    def buff_push(self,struct):
        self.struct_buff.append(struct)

    def send_push(self,struct):
        self.struct_send.append(struct)
    def send_pop(self,pos = 0):
        self.struct_send.pop(pos)
    def send_get(self,pos=0):
        try:
            return self.struct_send[pos]
        except IndexError as E:
            return False

    def isRunning(self,status=None):
        if(status == None):
            return self.is_running
        self.is_running = status