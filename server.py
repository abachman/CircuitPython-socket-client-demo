# pylint: skip-file
"""
Echo Server.

Usage:
    python server.py

    OR

    PORT=8080 python server.py

Binds to 0.0.0.0, so you may need to give it permission.
"""

from datetime import datetime
import signal
import sys
import os
import socket
from random import randint
import _thread

def ts():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def log(*args):
    print("[%s]" % ts(), ' '.join(map(str, args)))


class Server:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        port = os.getenv('PORT') or 10000
        server_address = ('0.0.0.0', port)
        log('starting up on %s port %s' % server_address)
        self.socket.bind(server_address)

        signal.signal(signal.SIGINT, self.close)

    def handle(self, connection, client_address):
        try:
            log('connection from', client_address)

            # Receive the data in small chunks and retransmit it
            while True:
                data = connection.recv(1024)
                log('received "%s"' % data)
                if data:
                    log('sending data back to the client')
                    connection.sendall(data)
                else:
                    log('no more data from', client_address)
                    break

        finally:
            # Clean up the connection
            connection.close()

        log("finished with", client_address)

    def close(self, *args):
        """Close the server down gracefully."""
        log("closing Server socket")
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
        except OSError as ex:
            log("socket.shutdown complained:", ex)
        self.socket.close()
        sys.exit(0)

    def run(self):
        """Run the server forever"""
        self.socket.listen(1)
        while True:
            # Wait for a connection
            log('waiting for a connection')
            connection, client_address = self.socket.accept()
            _thread.start_new_thread(self.handle, (connection, client_address))

if __name__ == '__main__':
    server = Server()
    server.run()
