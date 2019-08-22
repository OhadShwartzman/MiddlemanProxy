import threading
import socket
import config

class ServerReader(threading.Thread):
    '''
        This class will represent the proxy part which will read the messages from the server and send them to the client.
        it will simulate a client for the server. It will also run in a separate thread.
    '''
    def __init__(self, server_address, server_port):
        '''
            This function is the overloaded constructor of the class.
            it will connect to the server.
            input:
                the server's address, the server port
        '''
        threading.Thread.__init__(self)
        
        self.server_port = server_port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket = None # we will know in the future

        self.server_socket.connect((server_address, server_port))

    def run(self):
        while config.PROXY_RUN:
            server_data = self.server_socket.recv(config.MAX_PACKET_SIZE)
            if server_data:
                self.client_socket.sendall(server_data)
        self.server_socket.close()

    # SETTER for the server socket.
    def set_client_socket(self, client_socket):
        self.client_socket = client_socket
