import socket
import sys
import argparse
import logging
from threading import Thread
from webHttp.ResponseHandler import ResponseHandler

class WebServer(Thread):
    """ A simple web server implimentation """
    
    def __init__(self, rootPath, port): #should pass in a logging object, so the client could define how they want info returned
        
        logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-9s) %(message)s',)
        self.isStarted = False        
        self.filePath = rootPath
        self.port = port
        self.__urlHandlers = {}

        self.registerUrl("list", "UrlHandler")
        
        Thread.__init__(self)

    def run(self):
        
        self.isStarted = True

        try:
            self.sock = socket.socket()          
            logging.debug("Socket successfully created")
  
            self.sock.bind(('', self.port))         
            logging.debug(f"socket binded to {self.port}" )
  
            # put the socket into listening mode 
            self.sock.listen(5)      
            logging.debug("socket is listening")

            while self.isStarted:
                # Establish connection with client. 
                clientConn, addr = self.sock.accept()
                logging.debug("Received connection from %s:%s" % (addr))
                
                #thread off response handling so that we do not lock accepting new connections
                rh = ResponseHandler(clientConn, self.filePath, self.__urlHandlers)
                rh.start()

            self.sock.close()
        except:
            self.lastError = "An error occured while receiving client data. More info: %s" %(sys.exc_info()[1])
    
    def stop(self):
        self.isStarted = False

    def registerUrl(self, urlBaseName, urlHandlerClass):
        """ Register a url for custom script handling. Class.handleUrl will be called for the passed in class 
        
        
        Parameters
        ----------
        url : str
            Url base for your custom script. To invoke you would call "http://{webserver}:{port}.SCRIPT"
        urlHandlerClass : string
            String name of a derived class of urlHandler to invoke your custom code. You most override the handleUrl method

        """
        

        self.__urlHandlers[f"{urlBaseName.upper()}.SCRIPT"] = urlHandlerClass

