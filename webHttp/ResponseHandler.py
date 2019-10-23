import socket
import sys
import logging
from threading import Thread
from string import Template
from pathlib import Path
from webHttp import UrlHandler

class ResponseHandler(Thread):
    def __init__(self, clientConn, filePath, urlHandlers):
        self.clientConn = clientConn
        self.filePath = filePath
        self.urlHandlers = urlHandlers

        Thread.__init__(self)
    
    def handleClientRequest(self, conn, requestData):
        #Not sure if I can depend on all clients to format the request this way, but works in edge and chrome
        reqList = str(requestData).split('\r\n')

        #Not production code in the least, but for now I'm handling the GET request and ignoring everything else in the headers. 
        for i in reqList:
            splitReq = str(i).split(' ')
        
            fileIndex = 0

            for j in splitReq:
                fileIndex = fileIndex + 1
            
                if str(j)[:3] == "GET":
                    #Requested path will be the next thing specified after the GET
                    requestedFile = splitReq[fileIndex]
                    
                    #Check if we have a registered url handler for this request
                    
                    pageRequest = requestedFile[1:].upper()
                    
                    if pageRequest.find('?'):
                        # Has a querystring, so strip it and check if there is a url handler for this type
                        pageRequest = pageRequest[:pageRequest.find('?')]

                    if pageRequest in self.urlHandlers:
                        hcObj = self.urlHandlers[pageRequest]()
                        argumentsDict = {}
                        
                        if pageRequest == "LIST.SCRIPT":
                            # Built in list handler, needs filePath
                            argumentsDict = {"filePath": self.filePath}
                        else:
                            # Otherwise, we parse parameters from the get string
                            argumentsDict = self.parseQueryStringToDict(requestedFile)

                        pageContents = hcObj.handleUrl(argumentsDict)
                    else:
                        try:
                            #Path is the suggested file op object, as far as I've seen. os is getting deprecated.
                            pageContents = (Path(self.filePath) / pageRequest).read_text()

                        except:
                            template = Template(Path("template_not_found.html").read_text())
                            templateString = template.substitute(["fileName", requestedFile])
                            
                            response = f'HTTP/1.1 404 NOT FOUND\nContent-Type: text/html\n\n{templateString}\n'

                            conn.send(response.encode)
                            logging.debug("File %s not found" %(sys.exc_info()[1]))

                    conn.send(str.encode(f'HTTP/1.1 200 OK\nContent-Type: text/html\n\n{pageContents}'))
                break
                                            
    def run(self):
        __RESPONSE_TERMINATOR = b'\r\n\r\n'
        __RECIEVE_BUFFER = 1024

        try:
            doLoop = True
            fullResponse = ''
            while doLoop:
                data = self.clientConn.recv(__RECIEVE_BUFFER)
                fullResponse += data.decode("utf-8")

                if data[-4:] == __RESPONSE_TERMINATOR:
                    doLoop = False
            
            logging.debug(f"Received the following data:\n\r\n\r{fullResponse}")
            self.handleClientRequest(self.clientConn, fullResponse)
        
        except:
            logging.debug(f"Errored while reading in client data. More info: {sys.exc_info()[1]}")
        
        finally:
            self.clientConn.close()


    def parseQueryStringToDict(self, url):
        # Querystring would look something like "/test.html?param1=1&param2=2"
        paramDict = {}
        try:
            offset = url.find('?')
            if offset > 0:
                queryStringArr = str(url[offset + 1:]).split('&')
                for p in queryStringArr:
                    f = str(p).split('=')
                    paramDict[f[0]] = f[1]

        finally:
            return paramDict