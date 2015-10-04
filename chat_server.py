from argparse import ArgumentParser
import asyncio
from sys import argv

clients = []

class ChatServer(asyncio.Protocol):
  def connection_made(self, transport):
    self.transport = transport
    self.peername = transport.get_extra_info("peername")
    print("connection_made: {}".format(self.peername))
    clients.append(self)

  def data_received(self, data):
    print("data_received: {}".format(data.decode()))
    for client in clients:
      if client is not self:
        client.transport.write("{}: {}".format(self.peername, data.decode()).encode())

  def connection_lost(self, ex):
    print("connection_lost: {}".format(self.peername))
    clients.remove(self)

parser = ArgumentParser(description='Chat Client Python3 Script')
parser.add_argument('--host', dest='host', type=str, help='Host IP Address', default='127.0.0.1')
parser.add_argument('--port', dest='port', type=int, help='Host Port Number', default=8888)
args = parser.parse_args()
loop = asyncio.get_event_loop()
coro = loop.create_server(ChatServer, args.host, args.port)
server = loop.run_until_complete(coro)
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
  loop.run_forever()
except KeyboardInterrupt:
  pass
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
