import threading
import socket
import config

class ClientReader(threading.Thread):
    '''
        This class defines the thread which will simulate a server talking to the client, but in reality it will 
        Send the messages sent from the client to a parser and simply pass the messages to another thread which will
        send them to the actual server.
    '''
    def __init__(self, host_addr, port, parser_queue, queue_condition):
        '''
            This function is the overloaded constructor of the class Thread. It will run as a seperate thread.
            It will listen to and connect to the client
            input:
                the address of our simulated server, the port to listen to.
                the queue to pass the parsed data to, the lock to the queue.
        '''
        threading.Thread.__init__(self) # Call the constructor of the class we inherited from

        self.queue = parser_queue
        self.q_lock = queue_condition

        listening_socket = socket.socket(AF_INET, socket.SOCK_STREAM)

        # Will prevent bugs where the socket is already in use, etc
        listening_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listening_socket.bind((host_addr, port))
        listening_socket.listen(1) # we're just looking for 1 client

        self.client_port = port
        self.client_socket, self.client_address = listening_socket.accept() # Now we got the client!
        self.server_socket = None # Will be defined in the future. 

    def run(self):
        '''
            This function is the overloaded function from the function threading.Thread.run.
        '''
        while config.PROXY_RUN:
            client_data = self.client_socket.recv(config.MAX_PACKET_SIZE)
            if client_data:
                '''This segment will get hold of the shared queue, add it's message, notify the parser thread and then
                   It will release the queue. '''
                self.q_lock.acquire()
                self.queue.append((self.client_address, client_data.hex()))
                self.q_lock.notifyAll()
                self.q_lcok.release()
                # Pass the data on to the server.
                self.server_socket.sendall(client_data)
            self.client_socket.close()


    # SETTER FOR FIELD 'server_socket' important for communicating with the server.
    def set_server_socket(self, server_socket):
        self.server_socket = server_socket

    # GETTER FOR FIELD 'client_socket'
    def get_client_socket(self):
        return self.client_socket