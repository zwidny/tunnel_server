# Echo server program
import socket
import sys
import logging
import socketserver
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer

logging.basicConfig(level=logging.INFO)


class TunnelHTTPRequestHandler(BaseHTTPRequestHandler):
    def handle_client_request(self):
        """处理来自client的请求

        :return:
        """
        pass

    def handle(self):
        """Handle multiple requests if necessary."""
        self.close_connection = True

        self.handle_one_request()
        while not self.close_connection:
            self.handle_one_request()

    def handle_one_request(self):
        """Handle a single HTTP request.

        You normally don't need to override this method; see the class
        __doc__ string for information on how to handle specific HTTP
        commands such as GET and POST.

        """
        try:
            self.raw_requestline = self.rfile.readline(65537)
            if len(self.raw_requestline) > 65536:
                self.requestline = ''
                self.request_version = ''
                self.command = ''
                self.send_error(HTTPStatus.REQUEST_URI_TOO_LONG)
                return
            if not self.raw_requestline:
                self.close_connection = True
                return
            if not self.parse_request():
                # An error code has been sent, just exit
                return
            mname = 'do_' + self.command
            if not hasattr(self, mname):
                self.send_error(
                    HTTPStatus.NOT_IMPLEMENTED,
                    "Unsupported method (%r)" % self.command)
                return
            method = getattr(self, mname)
            method()
            self.wfile.flush()  # actually send the response if not already done.
        except socket.timeout as e:
            # a read or a write timed out.  Discard this connection
            self.log_error("Request timed out: %r", e)
            self.close_connection = True
            return


def test(HandlerClass=BaseHTTPRequestHandler,
         ServerClass=HTTPServer, protocol="HTTP/1.0", port=8000, bind=""):
    """Test the HTTP request handler class.

    This runs an HTTP server on port 8000 (or the port argument).

    """
    server_address = (bind, port)

    HandlerClass.protocol_version = protocol
    httpd = ServerClass(server_address, HandlerClass)

    sa = httpd.socket.getsockname()
    logging.info("Serving HTTP on", sa[0], "port", sa[1], "...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logging.info("\nKeyboard interrupt received, exiting.")
        httpd.server_close()
        sys.exit(0)


class TunnelBaseRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        logging.info('handle')

if __name__ == '__main__':
    HOST = 'localhost'
    PORT = 8000
    server = socketserver.TCPServer((HOST, PORT), TunnelBaseRequestHandler)
    server.serve_forever()
