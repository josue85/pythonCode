from string import Template
from pathlib import Path

#Any other url handlers will need to subclass this and implement handleUrl
class UrlHandler:
    """ Class to handle special case urls to do specific things. Default is to list the contents of the web directory """
    
    #Argument names and values will be based on the query string of the url and passed in as keyword arguments
    def handleUrl(self, params):
        """
        Method called when your registered url is hit. Pa


        Parameters
        ----------
        params : dictionary
            Parameters based on the query string of the URL

        """
        filePath = params["filePath"]
        path = Path(filePath)
        linkHtml = ""

        for file in path.glob("*.html"):
            linkHtml += f"<a href='{file.name}'>{file.name}</a><br>"

        template = Template(Path("template_directory.html").read_text())
        return template.substitute({"filePath": filePath, "urlList": linkHtml})
                            
        


