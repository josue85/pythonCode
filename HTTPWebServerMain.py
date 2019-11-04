import argparse
import logging
import sys
from webHttp.WebServer import WebServer
from webHttp.UrlHandler import UrlHandler
from webHttp.FileRequestHandler import FileRequestHandler
from string import Template
from pathlib import Path
import time

# Test my plugin. Not super useful, but redirects to the page requested in the query. For those with refined tastes who don't like typing in urls straight to the browser bar
class urlHandleRedirect(UrlHandler):
    def __init__(self):
        self.template = Template(Path("template_redirect.html").read_text())
    
    def handleUrl(self, parameter_list):
        url = parameter_list["url"]
        return self.template.substitute({"url": url})

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("rootPath", action="store")
    parser.add_argument("-p", "--port", help="set the port that http requests will be completed on", default=80, type=int)

    args = parser.parse_args()

    try:
        path = args.rootPath
        logging.debug(f"Serving files from {args.rootPath}")

    except:
        # no root path provided, nothing to do
        logging.debug("Hey bro, I heard you like not passing in parameters, hope you enjoy this hot can of nothing happening...")
        sys.exit()

    if args.port:
        port = args.port

    # FileRequestHandler will be responsible for serving the web page requests
    dfh = FileRequestHandler(path)
    ws = WebServer(dfh, port)

    ws.registerUrl("REDIRECT", urlHandleRedirect)

    ws.start()

    # time.sleep(10)
    
    # ws.stop()