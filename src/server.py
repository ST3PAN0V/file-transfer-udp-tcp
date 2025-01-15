from config import *

import socket
from os.path import abspath
import sys

class UDPServer:
    """A UDP server for sending file to a client."""

    def __init__(self, file_path: str, host: str = SERVER_HOST, port: int = SERVER_PORT):
        """Init the UDP server with the filename, host, and port."""
        self.file_path = file_path
        self.host = host
        self.port = port
        self.sock = None

    def _send_file(self, addr: tuple):
        """Sends the content of a file to the client socket."""
        try:
            with open(self.file_path, 'rb') as file:
                print("sending...")
                while True:
                    data = file.read(BUFFER)
                    if not data:
                        break
                    self.sock.sendto(data, addr)
                print(f"finished sending to {addr[0]}:{addr[1]}")
        except FileNotFoundError:
            print(f"Error: File '{self.file_path}' not found")
        except Exception as exc:
            print(f"Error: {exc}")

    def run(self):
        """Starts the UDP server, waits for a client connection, and sends the file's data."""
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.bind((self.host, self.port))
            print(f"serving {abspath(self.file_path)}", flush=True)
            data, addr = self.sock.recvfrom(BUFFER)
            print(f"request from {addr[0]}:{addr[1]}")
            self._send_file(addr)
        except Exception as exc:
            print(f"Error: {exc}")
        finally:
            self.sock.close()


def main():
    """Main function. Start server."""

    if len(sys.argv) != 2:
        print("Usage: python server.py <file_name>")
        return 1

    file_path = sys.argv[1]
    server = UDPServer(file_path=file_path)
    server.run()
    return 0


if __name__ == "__main__":
    main()