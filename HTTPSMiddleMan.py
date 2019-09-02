import MiddleMan
import ssl
import config
import socket
import HTTPSServerThread

class HTTPS_MiddleMan(MiddleMan.MiddleMan):
    '''
        This class in an inherited class from the Original http middleman class, which implements everything but in HTTPS.
        It will initialize an ssl socket, listen to new clients and open threads which will listen to them and pass 
        to the webserver via HTTPS protocol.
    '''
    def __init__(self, host_port, host_address):
        '''
            This function is the constructor for the class HTTPS_MiddleMan, it will initalize the whole socket - including the 
            whole ssl server.
        '''
        # Everything is taken from the original class except the socket now supports SSL.
        MiddleMan.MiddleMan.__init__(self, host_port, host_address)
        self.ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        self.ssl_context.load_cert_chain(config.CERT_FILE, config.KEY_FILE)
    
    def run():
        self.parser_thread.start()

        listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        listening_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listening_socket.bind((self.host_address, self.host_port))
        listening_socket.listen(5)
        s_sock = self.context.wrap_socket(listening_socket, server_side=True)

        # Wait for new clients
        while self.running:
            client_socket, client_address = listening_socket.accept()
            # Now, open a new SSL connection with the user
            # We define the connection as an SSL connection with the last parameter of the constructor - 
            # We pass the class of the server communicator, in this case it will be the HTTPS supported one.
            new_connection = ClientProxThread.ClientReader(client_socket, client_address, self.shared_queue, self.queue_lock, HTTPSServerThread.HTTPS_ServerReader)
            self.client_threads.append(new_connection)
            new_connection.start()

        self.parser_thread.join()
        for connection in self.client_threads:
            connection.stop_thread()
            connection.join()