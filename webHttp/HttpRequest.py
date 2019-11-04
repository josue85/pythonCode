from enum import Enum
from socket import socket

class HttpRequestTypes(Enum):
    GET = 1
    POST = 2
    PUT = 3
    HEAD = 4
    DELETE = 5
    PATCH = 6
    OPTIONS = 7


class HttpRequest():
    @staticmethod
    def isResponseReady():
        pass

    def __init__(self, requestData):
        self._headersList = requestData.split('\r\n')

        # For now only the GET request is handled
        for i in self._headersList:
            splitReq = i.split(' ')
        
            fileIndex = 0

            for fileIndex, curRequest in enumerate(splitReq, start=1):
            
                if curRequest[:3] == "GET":
                    self._requestType = HttpRequestTypes.GET

                    # Requested path will be the next thing specified after the GET
                    self._fullFilePath = splitReq[fileIndex]
                    
                    self._pageNameOnly = self.fullFilePath[1:].upper()
                    
                    if self._fullFilePath.find('?') > -1:
                        # Has a querystring, so strip it and check if there is a url handler for this type
                        queryString = self._fullFilePath[:self._fullFilePath('?')]
                        
                        # parse parameters from the get string
                        self._argumentsDict = self.parseQueryStringToDict(queryString)
                    
                    break
                

    def parseQueryStringToDict(self, url):
        # Querystring would look something like "/test.html?param1=1&param2=2"
        paramDict = {}
        try:
            offset = url.find('?')
            if offset > 0:
                queryStringArr = url[offset + 1:].split('&')
                for p in queryStringArr:
                    f = p.split('=')
                    paramDict[f[0]] = f[1]

        finally:
            return paramDict
    
    @property
    def requestType(self):
        return self._requestType
    
    @property
    def fullFilePath(self):
        return self._fullFilePath
    
    @property
    def pageNameOnly(self):
        return self._pageNameOnly
    
    @property
    def parametersDict(self):
        return self._argumentsDict
    
    @property
    def headers(self):
        return self.headers

