from argparse import ArgumentParser
import asyncio
from sys import stdin, exit, argv

class tcpclient:
  def __init__(self, reader, writer):
    self.writer = writer
    self.reader = reader
  
  @asyncio.coroutine
  def recv(self):
    return (yield from self.reader.read(100)).decode()
  
  @asyncio.coroutine
  def send(self, msg):
    self.writer.write(msg.encode())

@asyncio.coroutine
def chat_recv(socket):
  while True:
    echo = yield from socket.recv()
    if echo is None: break
    print ("%s"%echo)

@asyncio.coroutine
def chat_send(socket):
  reader = asyncio.StreamReader()
  yield from asyncio.get_event_loop().connect_read_pipe(lambda: asyncio.StreamReaderProtocol(reader), stdin)
  while True:
    msg = (yield from reader.readline()).decode('utf-8').strip('\r\n')
    if msg == "quit": exit()
    yield from socket.send(msg)

@asyncio.coroutine
def chat(loop,host,port):
  reader, writer = yield from asyncio.open_connection(host, port, loop=loop)
  client = tcpclient(reader, writer)
  tasks = [chat_recv(client), chat_send(client)]
  yield from asyncio.wait(tasks)

#if len(argv) > 1: host = argv[1]
#else: host = '127.0.0.1'
#if len(argv) > 2: port = int(argv[2])
#else: port = 8888
parser = ArgumentParser(description='Chat Client Python3 Script')
parser.add_argument('--host', dest='host', type=str, help='Host IP Address', default='127.0.0.1')
parser.add_argument('--port', dest='port', type=int, help='Host Port Number', default=8888)
args = parser.parse_args()
loop = asyncio.get_event_loop()
loop.run_until_complete(chat(loop,args.host,args.port))
loop.close()
