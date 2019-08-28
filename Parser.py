import threading
import config

class Parser(threading.Thread):
    '''
        This class defines the parser object, which will run in the background and parse all the data which is sent
        by the different connections.
    '''
    def __init__(self, parsing_queue, parsing_lock):
        '''
            This function is the constructor of the class Parser. It will initiallize the object.
            It also overloads the constructor of the inherited class threading.Thread
            input:
                the queue of data to parse, the lock which protects the queue.
        '''
        threading.Thread.__init__(self)

        self.queue = parsing_queue
        self.lock = parsing_lock
        self.running = True
    
    def run(self):
        '''
            This function will occur when the thread is set to start. it will go over the queue always and parse the text
            inside of it.
            input:
                none
        '''

        PACKET_IP_INDEX = 0
        PACKET_DATA_INDEX = 1
        # Run while the proxy is running.
        while config.DEBUG and self.running:
            self.lock.acquire()
            while not self.queue:
                # Wait to be notified of a new packet in the queue
                self.lock.wait()
            for packet in self.queue:
                print("{} : {}".format(packet[PACKET_IP_INDEX], packet[PACKET_DATA_INDEX]))
                self.queue.remove(packet)
            self.lock.release() 

    def stop_thread(self):
        self.running = False