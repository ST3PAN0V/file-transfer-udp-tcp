from config import *

import socket
from os.path import abspath
import sys

class TCPServer:
    """
    A TCP server for sending file to a client.
    """

    def __init__(
                 self,
                 file_path: str, 
                 host: str = SERVER_HOST, 
                 port: int = SERVER_PORT
                 ):
        """
        Init the TCP server with the filename, host, and port.
        """
        self.file_path = file_path
        self.host = host
        self.port = port
        self.sock = None

    def _send_file(self, conn: socket.socket):
        """
        Sends the content of a file to the client socket.
        """
        try:
            with open(self.file_path, 'rb') as file:
                print("sending...")
                while True:
                    data = file.read(BUFFER)
                    if not data:
                        break
                    conn.send(data)
            print("finished sending to",
                  f"{conn.getpeername()[0]}:{conn.getpeername()[1]}")
        except FileNotFoundError:
            print(f"Error: File '{self.file_path}' not found.")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.close()

    def run(self):
        """
        Starts the TCP server, waiting for a client connection,
        and sends the file's data.
        """
        try:
            self.sock = socket.socket(
                                      socket.AF_INET,
                                      socket.SOCK_STREAM
                                      )
            self.sock.bind((self.host, self.port))
            self.sock.listen(1)
            print("serving", abspath(self.file_path), flush=True)
            conn, addr = self.sock.accept()
            print("request from", f"{addr[0]}:{addr[1]}")
            self._send_file(conn)
        except Exception as exc:
            print(f"Error: {exc}")
        finally:
            self.sock.close()


def main():
    """
    Main function. Start server.
    """
    if len(sys.argv) != 2:
        print("Usage: python server_tcp.py <file_name>")
        return

    file_path = sys.argv[1]
    server = TCPServer(file_path=file_path)
    server.run()
    return 0


if __name__ == "__main__":
    main()

