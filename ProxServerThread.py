import threading
import socket
import config

class ServerReader(threading.Thread):
    '''
        This class will represent the proxy part which will read the messages from the server and send them to the client.
        it will simulate a client for the server. It will also run in a separate thread.
    '''
    def __init__(self, server_address, server_port, parser_queue, queue_lock, client_socket):
        '''
            This function is the overloaded constructor of the class.
            it will connect to the server.
            input:
                the server's address, the server port
        '''
        DEFAULT_PORT = 80
        threading.Thread.__init__(self)

        self.server_ip = socket.gethostbyname(server_address) # For passing on to the parser later
        self.server_address = server_address
        self.queue = parser_queue
        self.q_lock = queue_lock
        
        self.server_port = server_port
        if not self.server_port:
            self.server_port = DEFAULT_PORT

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket = None # we will know in the future

        self.server_socket.connect((self.server_address, self.server_port))
        self.running = True
        self.client_socket = client_socket

    def run(self):
        server_data = 1
        while self.running and server_data:
            try:
                server_data = self.server_socket.recv(config.MAX_PACKET_SIZE)
                if server_data:
                    '''
                    self.q_lock.acquire()
                    self.queue.append((self.server_address, server_data))
                    self.q_lock.notifyAll()
                    self.q_lock.release()'''
                    self.client_socket.sendall(server_data)
            except BrokenPipeError:
                break
        self.server_socket.close()

    # SETTER for the client socket.
    def set_client_socket(self, client_socket):
        self.client_socket = client_socket

    # GETTER FOR FIELD 'server_socket'
    def get_server_socket(self):
        return self.server_socket

    def stop_thread(self):
        self.running = False