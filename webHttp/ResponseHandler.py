import socket
import sys
import logging
from threading import Thread
from pathlib import Path
from webHttp import UrlHandler
from webHttp import FileRequestHandler
from webHttp import HttpRequest


class ResponseHandler(Thread):
    def __init__(self, fileRequestHandler, urlHandlers):
        self.urlHandlers = urlHandlers
        self.fileRequestHandler = fileRequestHandler

        Thread.__init__(self)
    
    def handleClientRequest(self, httpRequest:HttpRequest):
        
        if httpRequest.requestType == HttpRequest.HttpRequestTypes.GET:

            if httpRequest.pageNameOnly in self.urlHandlers:
                hcObj = self.urlHandlers[httpRequest.pageNameOnly]()
                argumentsDict = {}
                
                if httpRequest.pageNameOnly == "LIST.SCRIPT":
                    # Built in list handler, needs filePath
                    argumentsDict = {"filePath": self.fileRequestHandler.filePath}
                else:
                    # Otherwise, use the httpRequest object arguments dictionary 
                    argumentsDict = httpRequest.parametersDict

                pageContents = hcObj.handleUrl(argumentsDict)
                returnCode = 200
            else:
                returnCode, pageContents = self.fileRequestHandler.serveFile(httpRequest.pageNameOnly)                  

            return str.encode(f'HTTP/1.1 {returnCode} OK\nContent-Type: text/html\n\n{pageContents}')
        # Handle Post, PUT, etc here