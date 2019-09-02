import ProxServerThread
import ssl
import socket

class HTTPS_ServerReader(ProxServerThread.ServerReader):
    '''
        This class is the inherited class from ProxServerThread.ServerReader, it will utilize
        the same function as the original but it will do so with the SSL connection to utilize HTTPS.
        the only thing we really need to change is the constructor, it will initialize the ssl socket and created
        a wrapped one which acts the same as normal.
    '''
    def __init__(self, server_address, server_port, parser_queue, queue_lock):
        self.context = ssl.create_default_socket()
        self.queue = parser_queue
        self.q_lock = queue_lock

        self.server_port = server_port
        self.server_address = server_address
        self.un_server_socket = socket.create_connection((self.server_address, self.server_port))
        self.server_socket.settimeout(1000)
        self.server_socket = context.wrap_socket(self.server_socket, server_hostname=self.server_address)
        self.running = True
    def run():
        ProxServerThread.ServerReader.run(self)

    