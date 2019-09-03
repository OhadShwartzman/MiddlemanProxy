import ProxServerThread
import ssl
import socket
import threading
import config

class HTTPS_ServerReader(ProxServerThread.ServerReader):
    '''
        This class is the inherited class from ProxServerThread.ServerReader, it will utilize
        the same function as the original but it will do so with the SSL connection to utilize HTTPS.
        the only thing we really need to change is the constructor, it will initialize the ssl socket and created
        a wrapped one which acts the same as normal.
    '''
    def __init__(self, server_address, server_port, parser_queue, queue_lock, client_socket):
        DEFAULT_PORT = 443
        self.queue = parser_queue
        self.q_lock = queue_lock
        
        self.server_port = server_port
        self.server_address = server_address

        if not self.server_port:
            self.server_port = DEFAULT_PORT
        ProxServerThread.ServerReader.__init__(self, self.server_address, self.server_port, self.queue, self.q_lock, client_socket)
        
        self.server_socket = ssl.wrap_socket(self.server_socket, keyfile=config.KEY_FILE, certfile=config.CERT_FILE, server_side=False)
        self.client_socket = client_socket
        # The client has sent us a CONNECT method packet, because this operates as a HTTPS proxy,
        # We need to respond accordingly.
        self.client_socket.sendall(config.HTTPS_CONNECTION_SUCCESSFUL)

    def run(self):
        ProxServerThread.ServerReader.run(self)

    