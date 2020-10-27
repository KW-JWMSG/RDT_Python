from .modules.RdtController.RdtClient import RdtClient
from .modules.GbnController.GbnClient import GbnClient
from .modules.SrController.SrClient import SrClient

class Client:
    def __init__(self, messages):
        self.messages = messages

    def run_sr_class(self):
        self.data_class = SrClient()
    
    def run_gbn_class(self):
        self.data_class = SrClient()
    
    def run_rdt_class(self):
        self.data_class = SrClient()