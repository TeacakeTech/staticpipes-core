import http.server
import logging


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)


DIRECTORY = None

logger = logging.getLogger(__name__)


def server(directory_name, server_address, server_port):
    global DIRECTORY
    DIRECTORY = directory_name
    httpd = http.server.HTTPServer((server_address, server_port), Handler)
    logger.info("serving at http://" + server_address + ":" + str(server_port))
    httpd.serve_forever()
