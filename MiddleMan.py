import socket
import threading
import ClientProxThread
import ProxServerThread
import Parser
import config

class MiddleMan(threading.Thread):

    def __init__(self, host_port, host_address, server_port, server_address):
        '''
            This function is the constructor for the class Middleman, it will overload the constructor of the class
            threading.Thread, but still call it since we need to construct the 'Thread' part of the object.
            input:
                the port of the client, the address which the client will access for the proxy,
                the main server's port and the server's ip address.
        '''
        threading.Thread.__init__(self)

        self.shared_queue = []
        self.queue_lock = threading.Condition()
        
        self.parser_thread = Parser.Parser(self.shared_queue, self.queue_lock)

        self.client_connection = ClientProxThread.ClientReader(host_addr, host_port, self.shared_queue, self.queue_lock)
        self.server_connection = ProxServerThread.ServerReader(server_address, server_port, self.shared_queue, self.queue_lock)

        # We need to cross the sockets between the connections - since the one does not know currently of the other
        self.client_connection.set_server_socket(self.server_connection.get_server_socket())
        self.server_connection.set_client_socket(self.client_connection.get_client_socket())

    def run(self):
        '''
            This function will be called when the thread is set to start. It will start both threads (server & client connection)
            it will then wait for both connections to end.
            input:
                none
            output:
                none
        '''
        self.client_connection.start()
        self.server_connection.start()
        self.parser_thread.start()
        
        self.client_connection.join()
        self.server_connection.join()
        self.parser_thread.join()


    
