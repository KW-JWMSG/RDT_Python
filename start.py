from config import config 
from src.server import Server
from src.client import Client
import sys

def main():
    if len(sys.argv) < 2:
        return print('모드를 입력하세요')
    if(sys.argv[1] == 'server'):
        sv = Server(config)
    elif(sys.argv[1] == 'client'):
        cl = Client(config, range(400))

if __name__ == '__main__':
    main()
