from config import *

import socket
from os.path import abspath
import sys
import time

class UDPClient:
    """A UDP client for receiving files from a server."""

    def __init__(self, file_path: str, host: str = SERVER_HOST, port: int = SERVER_PORT):
        """Init the UDP client with the file_path, host, and port."""
        self.file_path = file_path
        self.host = host
        self.port = port
        self.sock = None

    def _receive_file(self):
        """Receives content from the server and writes it to the file."""
        try:
            with open(self.file_path, 'wb') as file:
                print("downloading...")
                start_time = time.time()
                while True:
                    try:
                        self.sock.settimeout(TIMEOUT)
                        data, _ = self.sock.recvfrom(BUFFER)
                        if not data:
                            break
                        file.write(data)
                        start_time = time.time() # Reset timer
                    except socket.timeout:
                        break

                print(f"downloaded as {abspath(self.file_path)}", flush=True)
        except Exception as exc:
            print(f"Error: {exc}")

    def run(self):
        """Connects to the server and receives the file."""
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.sendto(b"init", (self.host, self.port))
            print(f"requesting from {self.host}:{self.port}")
            self._receive_file()
        except Exception as exc:
            print(f"Error: {exc}")
        finally:
            self.sock.close()


def main():
    """Main function. Start client."""
    if len(sys.argv) != 2:
        print("Usage: python client.py <file_name>")
        return 1

    file_path = sys.argv[1]
    client = UDPClient(file_path=file_path)
    client.run()
    return 0


if __name__ == "__main__":
    main()