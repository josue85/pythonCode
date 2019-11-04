import socket
import sys
import argparse
import logging
from threading import Thread
from webHttp.ResponseHandler import ResponseHandler
from webHttp.UrlHandler import UrlHandler
from webHttp.FileRequestHandler import FileRequestHandler
from webHttp import HttpRequest
import select
import queue

class WebServer(Thread):
    """ A simple web server implimentation. Currently only web get is implemented  """
    
    def __init__(self, defaultFileHandler, port):
        
        self.isStarted = False        
        self.port = port
        self.__urlHandlers = {}
        self.defaultFileHandler = defaultFileHandler
        self.registerUrl("list", UrlHandler)
        
        Thread.__init__(self)

    def run(self):
        
        self.isStarted = True
        self.sock = socket.socket()          
        inputs = [ self.sock ]
        outputs = []
        messageQueue = {}

        try:
            self.sock.bind(('', self.port))         
            logging.debug(f"socket binded to {self.port}" )
  
            # put the socket into listening mode 
            self.sock.listen(5)      
            logging.debug("socket is listening")

            self.sock.setblocking(False)

        
            while inputs and self.isStarted:
                readable, writable, exceptional = select.select(inputs, outputs, inputs, 5)

                # inputs
                for s in readable:
                    if s is self.sock:
                        connection, client_address = s.accept()
                        logging.debug(f"Connection recieved from {client_address}")

                        connection.setblocking(False)
                        inputs.append(connection)
                        messageQueue[connection] = queue.Queue()

                    else:
                        data = s.recv(1024)
                        if data:
                            messageQueue[s].put(data)
                            if s not in outputs:
                                outputs.append(s)
                        else:
                            # readable socket with no data is a disconnect
                            if s in outputs:
                                outputs.remove(s)
                            inputs.remove(s)
                            s.close()

                            del messageQueue[s]

                # outputs
                for s in writable:
                    try:
                        nextMessage = messageQueue[s].get_nowait()
                    except:
                        if s in outputs:
                            outputs.remove(s)
                    
                    else:
                        # create a request object that will store a representation of the request
                        httpReq = HttpRequest.HttpRequest(nextMessage.decode("utf8"))
                        
                        rh = ResponseHandler(self.defaultFileHandler, self.__urlHandlers)
                        responseBack = rh.handleClientRequest(httpReq)

                        s.send(responseBack)
                        # s.close()
                        # outputs.remove(s)
                        # del messageQueue[s]

                # Exceptions
                for s in exceptional:
                    # be gone you 
                    inputs.remove(s)
                    if s in outputs:
                        outputs.remove(s)
                    s.close()

                    del messageQueue[s]

            # Web Server has been shut down
            sock.close() 
        
        except:
            self.lastError = "An error occured while receiving client data. More info: %s" %(sys.exc_info()[1])
    
    def stop(self):
        """ Stops the running web server. Please note that the web server may take up to 5 seconds to shut down. """

        
        logging.debug("webserver is shutting down")
        self.isStarted = False

    def registerUrl(self, urlBaseName, urlHandlerClass):
        """ Register a url for custom script handling. Class.handleUrl will be called for the passed in class 
        
        
        Parameters
        ----------
        url : str
            Url base for your custom script. To invoke you would call "http://{webserver}:{port}.SCRIPT"
        urlHandlerClass : class
            Derived class of urlHandler to invoke your custom code. handleUrl method will be invoked when the url is hit.

        """
        

        self.__urlHandlers[f"{urlBaseName.upper()}.SCRIPT"] = urlHandlerClass

