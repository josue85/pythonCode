import argparse
import logging
import sys
from webHttp.WebServer import WebServer
from webHttp.UrlHandler import UrlHandler
from string import Template
from pathlib import Path

# Test my plugin. Not super useful, but redirects to the page requested in the query. For those with refined tastes who don't like typing in urls straight to the browser bar
class urlHandleRedirect(UrlHandler):
    def handleUrl(self, parameter_list):
        url = parameter_list["url"]
        template = Template(Path("template_redirect.html").read_text())

        return template.substitute({"url": url})
        

#VS allows me to set the command line arguments, that's how I was testing
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

ws = WebServer(path, port)

ws.registerUrl("REDIRECT.SCRIPT", 'urlHandleRedirect')

ws.start()

if __name__ == '__main__':
    pass

