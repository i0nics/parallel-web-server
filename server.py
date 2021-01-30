#!/usr/bin/env python3
# Programmer: Bikram Chatterjee
# Parallel Web Server
import argparse
import datetime
import mimetypes
import os
import signal
import socket
import sys
import threading
import select


class Thread(threading.Thread):

    def __init__(self, client_s, args):
        threading.Thread.__init__(self)
        self.client_s = client_s
        self.args = args

    def run(self):
        client_s, args = self.client_s, self.args
        while True:
            raw_bytes = bytes()
            while not raw_bytes.endswith(bytes('\r\n\r\n', 'ascii')):
                try:
                    raw_bytes += client_s.recv(args.recv)
                    if len(raw_bytes) == 0:
                        close_s(client_s, args.verbose)
                        return

                except socket.error as msg:
                    if args.verbose:
                        print("Error: unable to recv()")
                        print("Description: " + str(msg))
                    sys.exit()

            request = raw_bytes.decode('ascii')
            if args.verbose:
                print("Received %d bytes from client\n" % len(raw_bytes))
                print("Message contents:", request.replace('\r\n\r\n', '\n'))

            re_split = request.split(' ')
            method, path, file, protocol = re_split[0], re_split[1], bytes('', 'ascii'), 'HTTP/1.1 '
            status_code = '200 OK' if method == 'GET' or method == 'HEAD' else '501 Request method not implemented'
            
            if status_code == '200 OK':
                try:
                    if path == '/':
                        path = '/index.html'
                    with open(args.base + path, "rb") as file:
                        response_headers = {
                            'Content-Length': os.path.getsize(args.base + path),
                            'Content-Type': mimetypes.guess_type(args.base + path)[0] + '; charset=utf-8',
                            'Date': datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT'),
                            'Expires': (datetime.datetime.utcnow() + datetime.timedelta(hours=12)).strftime('%a, %d %b %Y %H:%M:%S GMT'),
                            'Last-Modified': datetime.datetime.fromtimestamp(os.path.getmtime(args.base + path)).strftime('%a, %d %b %Y %H:%M:%S GMT'),
                            'Server': 'COMP 177 Python Multi-Thread\r\n'
                        }
                        response_headers_raw = ''.join('%s: %s\r\n' % (k, v) for k, v in response_headers.items())
                        send_data(client_s, bytes(protocol + status_code + '\r\n' + response_headers_raw, 'ascii'))

                        if method == 'GET':
                            while byte := file.read(64 * 1024):
                                send_data(client_s, byte)

                except (FileNotFoundError, IsADirectoryError):
                    status_code = '404 Not Found'

            if status_code != '200 OK':
                file = bytes('<html><body><center><h3 style="color:red; font-size:30px">Error ' + status_code +
                             '</h3><p>COMP 177 HTTP Server</p></center></body></html>', 'ascii')
                response_headers = {
                    'Content-Length': len(file),
                    'Date': datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT"),
                    'Server': 'COMP 177 Python Multi-Thread\r\n'
                }
                response_headers_raw = ''.join('%s: %s\r\n' % (k, v) for k, v in response_headers.items())
                send_data(client_s, bytes(protocol + status_code + '\r\n' + response_headers_raw, 'ascii') + file)

            if 'Connection: close' in request:
                close_s(client_s, args.verbose)
                return


def send_data(client_s, data):
    try:
        client_s.sendall(data)
    except (BrokenPipeError, ConnectionResetError):
        pass


# Close the client socket
def close_s(client_s, v):
    try:
        client_s.close()
        if v:
            print('Client socket closed\n')
    except socket.error as msg:
        if v:
            print('Error: unable to close() socket')
            print("Description: " + str(msg))
        sys.exit()


def main():

    # Handle CTRL+C to stop the program
    def signal_handler(sig, frame):
        print('\nExiting Gracefully. Please Wait Until All Requests Are Completed.')
        reading, writing, error = select.select([s], [], [], 1)
        if reading:
            try:
                (client_s, client_addr) = s.accept()
                if args.verbose:
                    print("Accepted incoming connection from client")
                    print("Client IP, Port = %s" % str(client_addr))

                client_t = Thread(client_s, args)
                client_t.start()

            except socket.error as msg:
                print("Error: unable to accept()")
                print("Description: " + str(msg))
                sys.exit()

        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    
    # Add command line arguments
    parser = argparse.ArgumentParser(description='Web Server for COMP/ECPE 177')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0', help='Show Program\'s Version Number and Exit')
    parser.add_argument('--base', metavar='BASE_DIR', default='website/html', help='Base dir Containing Website')
    parser.add_argument('--port', type=int, default=8080, help='Port Number to Listen On')
    parser.add_argument('--recv', type=int, default=64 * 1024, help='Receive Size to Accommodate Incoming Data From the Network')
    parser.add_argument('--verbose', action="store_true", help='Enable Debugging Output')
    args = parser.parse_args()

    # Create TCP socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    except socket.error as msg:
        print("Error: could not create socket")
        print("Description: " + str(msg))
        sys.exit()

    # Bind to listening port
    try:
        host = ''  # Bind to all interfaces
        s.bind((host, args.port))
    except socket.error as msg:
        print("Error: unable to bind on port %d" % args.port)
        print("Description: " + str(msg))
        sys.exit()

    # Listen
    try:
        backlog = 10  # Number of incoming connections that can wait to be accept()'ed before being turned away
        s.listen(backlog)
    except socket.error as msg:
        print("Error: unable to listen()")
        print("Description: " + str(msg))
        sys.exit()

    if args.verbose:
        print("Listening socket bound to port %d\n" % args.port)

    while True:
        try:
            # Accept incoming connection
            (client_s, client_addr) = s.accept()
            if args.verbose:
                print("Accepted incoming connection from client")
                print("Client IP, Port = %s" % str(client_addr))
                
            # Create and start a new thread
            client_t = Thread(client_s, args)
            client_t.start()

        except socket.error as msg:
            print("Error: unable to accept()")
            print("Description: " + str(msg))
            sys.exit()


if __name__ == "__main__":
    sys.exit(main())
