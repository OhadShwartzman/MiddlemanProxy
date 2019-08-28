import threading
import socket
import config

class ServerReader(threading.Thread):
    '''
        This class will represent the proxy part which will read the messages from the server and send them to the client.
        it will simulate a client for the server. It will also run in a separate thread.
    '''
    def __init__(self, server_address, server_port, parser_queue, queue_lock):
        '''
            This function is the overloaded constructor of the class.
            it will connect to the server.
            input:
                the server's address, the server port
        '''
        threading.Thread.__init__(self)

        self.server_address = server_address # For passing on to the parser later

        self.queue = parser_queue
        self.q_lock = queue_lock
        
        self.server_port = server_port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.settimeout(1000)
        self.client_socket = None # we will know in the future

        self.server_socket.connect((server_address, server_port))
        self.running = True

    def run(self):
        while self.running:
            try:
                server_data = self.server_socket.recv(config.MAX_PACKET_SIZE)
            except:
                break
            if server_data:
                '''
                self.q_lock.acquire()
                self.queue.append((self.server_address, server_data))
                self.q_lock.notifyAll()
                self.q_lock.release()'''
                self.client_socket.sendall(server_data)
        self.server_socket.close()

    # SETTER for the client socket.
    def set_client_socket(self, client_socket):
        self.client_socket = client_socket

    # GETTER FOR FIELD 'server_socket'
    def get_server_socket(self):
        return self.server_socket

    def stop_thread(self):
        self.running = False