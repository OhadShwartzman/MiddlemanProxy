import socket
import threading
import ClientProxThread
import ProxServerThread
import Parser
import config

class MiddleMan(threading.Thread):

    def __init__(self, host_port, host_address):
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

        self.host_port = host_port
        self.host_address = host_address

        self.client_threads = []
        self.running = True

    def run(self):
        '''
            This function will be called when the thread is set to start. It will start both threads (server & client connection)
            it will then wait for both connections to end.
            input:
                none
            output:
                none
        '''
        self.parser_thread.start()
        

        listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Will prevent bugs where the socket is already in use, etc
        listening_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listening_socket.bind((self.host_address, self.host_port))
        listening_socket.listen(5)
        
        while self.running:
            client_socket, client_address = listening_socket.accept() # Now we got the client!
            new_connection = ClientProxThread.ClientReader(client_socket, client_address, self.shared_queue, self.queue_lock, ProxServerThread.ServerReader)
            self.client_threads.append(new_connection)
            new_connection.start()

        listening_socket.close()
        self.parser_thread.stop_thread()

    def stop_thread(self):
        self.running = False
        for connection in self.client_threads:
            connection.stop_thread()

    
