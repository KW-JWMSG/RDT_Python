from .modules.RdtController.RdtServer import RdtServer
from .modules.GbnController.GbnServer import GbnServer
from .modules.SrController.SrServer import SrServer

class Server:
    def __init__(self, messages):
        self.messages = messages

    def run_sr_server(self):
        self.data_class = SrClient()
    
    def run_gbn_server(self):
        self.data_class = SrClient()
    
    def run_rdt_server(self):
        self.data_class = SrClient()