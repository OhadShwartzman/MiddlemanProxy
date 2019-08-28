
class HttpData:
    '''
        This class will automatically extract all the details of our http Request packet from 
        the bytes object sent to us via the socket.
    '''
    def __init__(self, data):
        self.data = data
        self.build_data()
    
    def build_data(self):
        text_data = self.data.decode('utf-8')

        text_lines = text_data.split('\r\n')
        # Handle the first line of the HTTP request, which is usually the most important one.
        first_line = text_lines[0]
        self.request_type, self.url, self.http_sig = first_line.split(' ')

        self.target_domain, self.target_port = self.parse_url(self.url)

    @staticmethod
    def parse_url(url):
        '''
            This function will recieve a url, parse it and return the domain and the port used.
            input:
                the url
            output:
                a tuple (domain, port)    

        EDGE CASE FOR URL:
            http://google.com/:8080 
            google.com
            we need to cover both cases.
        '''
        PROTOCOL_DOMAIN_SEPERATOR = '://'
        PORT_SEPERATOR = ':'
        DEFAULT_PORT = 80
        DOMAIN_END = '/'
        NOT_FOUND = -1

        protocol_loc = url.find(PROTOCOL_DOMAIN_SEPERATOR)
        if not protocol_loc == NOT_FOUND:
            url = url[protocol_loc + len(PROTOCOL_DOMAIN_SEPERATOR):] # We don't need the protocol in the url.
        
        port_loc = url.find(PORT_SEPERATOR)

        port = DEFAULT_PORT
        if not port_loc == NOT_FOUND:
            url, port = url.split(PORT_SEPERATOR)
            port = int(port)

        domain_end_loc = url.find(DOMAIN_END)
        domain = url
        if not domain_end_loc == NOT_FOUND:
            domain = url[:domain_end_loc]
        return (domain, port)


        # Go over the rest of the lines, read the headers and put them in another container.
        for line in text_lines[1:]:
            line.replace()