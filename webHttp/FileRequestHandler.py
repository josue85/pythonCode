from pathlib import Path
from string import Template

class FileRequestHandler():
    def __init__(self, filePath):
        self.filePath = filePath
        
        #Cache template files
        self.template = Template(Path("template_not_found.html").read_text())

    def serveFile(self, pageUrl):
        HTTP_OK_CODE = 200
        HTTP_FILE_NOT_FOUND_CODE = 404

        try:
            path = Path(self.filePath) / pageUrl
            return (HTTP_OK_CODE, path.read_text())
        except:
            templateString = self.template.substitute(["fileName", pageUrl])
            return (HTTP_FILE_NOT_FOUND_CODE, templateString)
            
            #response = f'HTTP/1.1 404 NOT FOUND\nContent-Type: text/html\n\n{templateString}\n'

            #conn.send(response.encode())
            #logging.debug("File %s not found" %(sys.exc_info()[1]))
            
