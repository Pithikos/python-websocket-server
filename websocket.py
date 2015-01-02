# Author: Johan Hanssen Seferidis
# License: MIT

import re, sys
import struct
from base64 import b64encode
from hashlib import sha1

if sys.version_info[0] < 3 :
	from SocketServer import ThreadingMixIn, TCPServer, StreamRequestHandler
else:
	from socketserver import ThreadingMixIn, TCPServer, StreamRequestHandler



class API():

	def run_forever(self):
		try:
			print("Listening on port %d for clients.." % self.port)
			self.serve_forever()
		except KeyboardInterrupt:
			self.server_close()
			print("Server terminated.")
		except Exception as e:
			print("ERROR: WebSocketsServer: "+str(e))
			exit(1)

	def new_client(self, client, server):
		pass
		print("New client connected and was given id %d" % client['id'])

	def client_left(self, client, server):
		pass
		print("Client(%d) disconnected" % client['id'])

	def message_received(self, client, server, message):
		pass
		print("Client(%d) said: %s" % (client['id'], message))

	def set_fn_new_client(self, fn):
		self.new_client=fn

	def set_fn_client_left(self, fn):
		self.client_left=fn

	def set_fn_message_received(self, fn):
		self.message_received=fn

	def send_message(self, client, msg):
		self._unicast_(client, msg)

	def send_message_to_all(self, msg):
		self._multicast_(msg)



class WebSocketsServer(ThreadingMixIn, TCPServer, API):

	allow_reuse_address = True
	daemon_threads = True # comment to keep threads alive until finished

	# clients is list of:
	#    {
	#     'id'      : id,
	#     'handler' : handler,
	#     'address' : (addr, port)
	#    }
	clients=[]
	id_counter=0

	def __init__(self, port, host='127.0.0.1'):
		self.port=port
		TCPServer.__init__(self, (host, port), WebSocketHandler)

	def _message_received_(self, handler, msg):
		self.message_received(self.handler_to_client(handler), self, msg)

	def _new_client_(self, handler):
		self.id_counter += 1
		client={
			'id'      : self.id_counter,
			'handler' : handler,
			'address' : handler.client_address
		}
		self.clients.append(client)
		self.new_client(client, self)
		
	def _client_left_(self, handler):
		client=self.handler_to_client(handler)
		self.client_left(client, self)
		self.clients.remove(client)
		
	def _unicast_(self, to_client, msg):
		to_client['handler'].send_message(msg)

	def _multicast_(self, msg):
		for client in self.clients:
			self._unicast_(client, msg)
		
	def handler_to_client(self, handler):
		for client in self.clients:
			if client['handler'] == handler:
				return client


class WebSocketHandler(StreamRequestHandler):

	def __init__(self, socket, addr, server):
		self.server=server
		StreamRequestHandler.__init__(self, socket, addr, server)

	def setup(self):
		StreamRequestHandler.setup(self)
		self.keep_alive = True
		self.handshake_done = False
		self.valid_client = False

	def handle(self):
		while self.keep_alive:
			if not self.handshake_done:
				self.handshake()
			elif self.valid_client:
				self.read_next_message()

	def read_next_message(self):
		b1 = self.rfile.read(1)
		b2 = self.rfile.read(1)
		FIN    = ord(b1) & 0b10000000
		OPCODE = ord(b1) & 0b00001111
		MASKED = ord(b2) & 0b10000000
		LENGTH = ord(b2) & 0b01111111

		if OPCODE == 8:
			print("Client asked to close connection.")
			self.keep_alive = 0
			return
		if not MASKED:
			print("Client must always be masked.")
			self.keep_alive = 0
			return

		length = LENGTH
		if LENGTH == 126:
			length = struct.unpack(">H", self.rfile.read(2))[0]
		elif LENGTH == 127:
			length = struct.unpack(">Q", self.rfile.read(8))[0]

		# python3 gives ordinal of byte directly
		if sys.version_info[0] < 3:
			masks = [ord(b) for b in self.rfile.read(4)]
		else:
			masks = [b for b in self.rfile.read(4)]

		decoded = ""
		for char in self.rfile.read(length):
			if isinstance(char, str): # python2 fix
				char = ord(char)
			char ^= masks[len(decoded) % 4]
			decoded += chr(char)
		self.server._message_received_(self, decoded)

	def send_message(self, message):
		self.send_text(message)
		
	def send_text(self, message):
		'''
		+-+-+-+-+-------+-+-------------+-------------------------------+
		 0                   1                   2                   3
		 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
		+-+-+-+-+-------+-+-------------+-------------------------------+
		|F|R|R|R| opcode|M| Payload len |    Extended payload length    |
		|I|S|S|S|  (4)  |A|     (7)     |             (16/64)           |
		|N|V|V|V|       |S|             |   (if payload len==126/127)   |
		| |1|2|3|       |K|             |                               |
		+-+-+-+-+-------+-+-------------+ - - - - - - - - - - - - - - - +
		|     Extended payload length continued, if payload len == 127  |
		+ - - - - - - - - - - - - - - - +-------------------------------+
		|                               | Masking-key, if MASK set to 1 |
		+-------------------------------+-------------------------------+
		| Masking-key (continued)       |          Payload Data         |
		+-------------------------------- - - - - - - - - - - - - - - - +
		:                     Payload Data continued ...                :
		+ - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
		|                     Payload Data continued ...                |
		+---------------------------------------------------------------+
		'''
		#   0 = '0x00' = 0b00000000
		# 125 = '0x7d' = 0b01111101
		# 126 = '0x7e' = 0b01111110
		# 127 = '0x7f' = 0b01111111
		# 128 = '0x80' = 0b10000000
		# 129 = '0x81' = 0b10000001
		length = len(message)
		
		# fits in one frame
		if length <= 125:
			self.request.send(b'\x81')
			self.request.send(chr(length).encode())
			self.request.send(message.encode())
			
		# fits in one frame but needs extended payload length
		elif length >= 126 and length <= 65535:
			self.request.send(b'\x81\x7f') # extended payload
			self.request.send(struct.pack(">Q", length))
			self.request.send(message.encode())
		
		# needs chunking
		else:
			chunk_size=65535
			for pos in range(0, length, chunk_size):
				chunk = message[pos:pos+chunk_size]
				if pos == 0:
					#print("sending first frame")
					self.request.send(b'\x01')
				elif length - pos != length % chunk_size:
					#print("sending middle frame")
					self.request.send(b'\x00')
				else:
					#print("sending last frame")
					self.request.send(b'\x80')
				if length <= 125:
					self.request.send(chr(len(chunk)).encode())
				else:
					self.request.send(b'\x7f')
					self.request.send(struct.pack(">Q", len(chunk)))
				self.request.send(chunk.encode())
		
	def send_binary(self, message):
		self.request.send(bytes(0b10000010))
		pass

	def handshake(self):
		message = self.request.recv(1024).decode().strip()
		upgrade = re.search('\nupgrade[\s]*:[\s]*websocket', message.lower())
		if not upgrade:
			self.keep_alive = False
			return
		key = re.search('\n[sS]ec-[wW]eb[sS]ocket-[kK]ey[\s]*:[\s]*(.*)\r\n', message)
		if key:
			key = key.group(1)
		else:
			print("Client tried to connect but was missing a key")
			self.keep_alive = False
			return
		response = self.make_handshake_response(key)
		self.handshake_done = self.request.send(response.encode())
		self.valid_client = True
		self.server._new_client_(self)
		
	def make_handshake_response(self, key):
		response = \
		  'HTTP/1.1 101 Switching Protocols\r\n'\
		  'Upgrade: websocket\r\n'              \
		  'Connection: Upgrade\r\n'             \
		  'Sec-WebSocket-Accept: %s\r\n'        \
		  '\r\n' % self.calculate_response_key(key)
		return response
		
	def calculate_response_key(self, key):
		GUID = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
		hash = sha1(key.encode() + GUID.encode())
		response_key = b64encode(hash.digest()).strip()
		return response_key.decode('ASCII')

	def finish(self):
		self.server._client_left_(self)


# This is only for testing purposes
class DummyWebsocketHandler(WebSocketHandler):
    def __init__(self, *_):
        pass
