import struct
from base64 import b64encode
from hashlib import sha1
from mimetools import Message
from StringIO import StringIO
from SocketServer import ThreadingMixIn, TCPServer, StreamRequestHandler



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

	def new_client(self):
		pass

	def client_left(self):
		pass

	def message_received(self):
		pass

	def set_fn_new_client(self, fn):
		self.new_client=fn

	def set_fn_client_left(self, fn):
		self.client_left=fn

	def set_fn_message_received(self, fn):
		self.message_received=fn

	def send_message(self, client_id, msg):
		self._unicast_(client_id, msg)

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

	def __init__(self, port, host='localhost'):
		self.port=port
		TCPServer.__init__(self, (host, port), WebSocketHandler)

	def _message_received_(self, handler, msg):
		self.message_received(self.handler_to_client(handler), msg)

	def _new_client_(self, handler):
		id=1
		if len(self.clients) > 0:
			id=len(self.clients)+1
		client={
			'id'      : id,
			'handler' : handler,
			'address' : handler.client_address
		}
		self.clients.append(client)
		self.new_client(client, self)
		
	def _client_left_(self, handler):
		# REMOVE CLIENT HERE
		client=self.handler_to_client(handler)
		self.client_left(client, self)
		self.clients.remove(client)
		
	def _unicast_(self, client_id, msg):
		for client in self.clients:
			if client_id == client['id']:
				client['handler'].send_message(msg)

	def _multicast_(self, msg):
		for client in self.clients:
			self._unicast_(client['id'], msg)
		
	def handler_to_client(self, handler):
		for client in self.clients:
			if client['handler'] == handler:
				return client



class WebSocketHandler(StreamRequestHandler):

	magic  = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
	server = None
	keep_alive = True

	def __init__(self, socket, addr, server):
		self.server=server
		StreamRequestHandler.__init__(self, socket, addr, server)

	def setup(self):
		StreamRequestHandler.setup(self)
		self.handshake_done = False

	def handle(self):
		while self.keep_alive:
			print(self.keep_alive)
			if not self.handshake_done:
				self.handshake()
			else:
				self.read_next_message()

	def read_next_message(self):
		length = ord(self.rfile.read(2)[1]) & 127
		if length == 126:
			lengih = struct.unpack(">H", self.rfile.read(2))[0]
		elif length == 127:
			length = struct.unpack(">Q", self.rfile.read(8))[0]
		masks = [ord(byte) for byte in self.rfile.read(4)]
		decoded = ""
		data=self.rfile.read(length)

		# handling protocol spec v76 (old non-hybi)
		if length == 2 and \
			ord(data[0]) ^ masks[0] == 3 and \
		    ord(data[1]) ^ masks[1] == 233:
				self.keep_alive = False
				return

		for char in data:
			char=ord(char) ^ masks[len(decoded) % 4]
			decoded += chr(char)
		self.server._message_received_(self, decoded)

	def send_message(self, message):
		self.request.send(chr(129))
		length = len(message)
		if length <= 125:
			self.request.send(chr(length))
		elif length >= 126 and length <= 65535:
			self.request.send(126)
			self.request.send(struct.pack(">H", length))
		else:
			self.request.send(127)
			self.request.send(struct.pack(">Q", length))
		self.request.send(message)

	def handshake(self):
		data = self.request.recv(1024).strip()
		headers = Message(StringIO(data.split('\r\n', 1)[1]))
		if headers.get("Upgrade", None) != "websocket":
			return
		key = headers['Sec-WebSocket-Key']
		digest = b64encode(sha1(key + self.magic).hexdigest().decode('hex'))
		response = 'HTTP/1.1 101 Switching Protocols\r\n'
		response += 'Upgrade: websocket\r\n'
		response += 'Connection: Upgrade\r\n'
		response += 'Sec-WebSocket-Accept: %s\r\n\r\n' % digest
		self.handshake_done = self.request.send(response)
		self.server._new_client_(self)
		
	def finish(self):
		self.server._client_left_(self)
		print("Closing connection")
