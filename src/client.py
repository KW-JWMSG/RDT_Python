from .modules.RDTProtocol.RdtClient import RdtClient

class Client:
    def __init__(self, config, message_pool):
        self.rdtClient = RdtClient(config['server_host'], config['server_port'], config['windows_size'], message_pool, timeout=config['client_timeout'])
    