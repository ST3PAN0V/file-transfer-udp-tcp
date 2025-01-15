from config import *

import socket
from os.path import abspath
import sys

class TCPClient:
    """
    A TCP client for receiving files from a server.
    """

    def __init__(
                 self, 
                 file_path: str, 
                 host: str = SERVER_HOST, 
                 port: int = SERVER_PORT
                 ):
        """
        Init the TCP client with the file_path, host, and port.
        """
        self.file_path = file_path
        self.host = host
        self.port = port
        self.sock = None

    def _receive_file(self):
        """
        Receives a content from the server and write it in file.
        """
        try:
            with open(self.file_path, 'wb') as file:
                print(f"downloading...")
                while True:
                    data = self.sock.recv(BUFFER)
                    if not data:
                        break
                    file.write(data)
                print("downloaded as", abspath(self.file_path), flush=True)
        except FileNotFoundError:
            print(f"Error: wrong path: '{self.file_path}'")
        except Exception as exc:
            print(f"Err: {exc}")
        finally:
            self.sock.close()

    def run(self):
        """
        Connects to the server and receiving file.
        """
        try:
            self.sock = socket.socket(
                                      socket.AF_INET, 
                                      socket.SOCK_STREAM
                                      )
            self.sock.connect((self.host, self.port))
            print(f"requesting from {self.host}:{self.port}")
            self._receive_file()
        except Exception as exc:
            print(f"Error: {exc}")
        finally:
            self.sock.close()

def main():
    """
    Main function. Start client.
    """
    if len(sys.argv) != 2:
        print("Usage: python client_tcp.py <file_name>")
        return

    file_path = sys.argv[1]
    client = TCPClient(file_path=file_path)
    client.run()
    return 0


if __name__ == "__main__":
    main()