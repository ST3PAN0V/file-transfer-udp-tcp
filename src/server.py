import socket
from os.path import abspath
import sys

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8080
BUFFER = 4096

class UDPServer:
    """
    A UDP server for sending file to a client.
    """

    def __init__(
                 self,
                 file_path: str, 
                 host: str = SERVER_HOST, 
                 port: int = SERVER_PORT
                 ):
        """
        Init the UDP server with the filename, host, and port.
        """
        self.file_path = file_path
        self.host = host
        self.port = port
        self.sock = None

    def _send_file(self, addr: tuple):
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
                    self.sock.sendto(data, addr)
            print("finished sending to", f"{addr[0]}:{addr[1]}")
        except Exception as e:
            print(f"Err: {e}")

    def run(self):
        """
        Starts the UDP server, waiting for a client connection,
        and sends the file's data.
        """
        try:
            self.sock = socket.socket(
                                      socket.AF_INET,
                                      socket.SOCK_DGRAM
                                      )
            self.sock.bind((self.host, self.port))
            print("serving", abspath(self.file_path), flush=True)
            data, addr = self.sock.recvfrom(BUFFER)
            print("request from", f"{addr[0]}:{addr[1]}")
            self._send_file(addr=addr)
        except Exception as exc:
            print(f"Err: {exc}")
        finally:
            self.sock.close()


def main():
    """
    Main function. Start server.
    """
    if len(sys.argv) != 2:
        print("Usage: python server.py <file_name>")
        return

    file_path = sys.argv[1]
    server = UDPServer(file_path=file_path)
    server.run()
    return 0


if __name__ == "__main__":
    main()

