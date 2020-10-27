from .modules.RDTProtocol.RdtServer import RdtServer

class Server:
    def __init__(self, config):
        self.rdtServer = RdtServer(config['server_host'], config['server_port'], config['windows_size'], timeout=config['server_timeout'],buffer_type=config['buffer_type'])
