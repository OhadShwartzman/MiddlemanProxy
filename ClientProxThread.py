import threading
import socket
import config
import Databuilder
import ProxServerThread

class ClientReader(threading.Thread):
    '''
        This class defines the thread which will simulate a server talking to the client, but in reality it will 
        Send the messages sent from the client to a parser and simply pass the messages to another thread which will
        send them to the actual server.
    '''
    def __init__(self, client_socket, client_address, parser_queue, queue_condition):
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

        self.client_socket = client_socket
        self.client_address = client_address
        self.server_thread = None
        self.running = True

    def run(self):
        '''
            This function is the overloaded function from the function threading.Thread.run.
        '''
        while self.running:
            try:
                client_data = self.client_socket.recv(config.MAX_PACKET_SIZE)
            except:
                break
            if client_data:
                '''This segment will get hold of the shared queue, add it's message, notify the parser thread and then
                   It will release the queue. '''
                http_request = Databuilder.HttpData(client_data)
                '''
                self.q_lock.acquire()
                self.queue.append((self.client_address, http_request))
                self.q_lock.notifyAll()
                self.q_lock.release()
                '''
                # Pass the data on to the server.
                domain = http_request.target_domain

                # If connection with this server has not been yet initiallized, open a thread of communication with this
                # server, set it's socket to be ours and start it.
                if not self.server_thread or not self.server_thread.isAlive():
                    self.server_thread = ProxServerThread.ServerReader(socket.gethostbyname(domain), http_request.target_port, self.queue, self.q_lock)
                    self.server_thread.set_client_socket(self.client_socket)
                    self.server_thread.start()

                    print("new domain")
                    print(domain)
                    print(http_request.target_port)
                self.server_thread.get_server_socket().sendall(client_data)

        # Wait for each server thread to stop, then close the socket
        if self.server_thread:
            self.server_thread.stop_thread()
            self.server_thread.join()
        
        self.client_socket.close()

    # GETTER FOR FIELD 'client_socket'
    def get_client_socket(self):
        return self.client_socket

    def stop_thread(self):
        self.running = False