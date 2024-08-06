import zmq
from rich import print

class TEMClient:
    _default_timeout = 1000 #1s

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.verbose = True

        self._set_default_timeout()

    def _set_default_timeout(self):
        self.socket.setsockopt(zmq.SNDTIMEO, TEMClient._default_timeout)
        self.socket.setsockopt(zmq.RCVTIMEO, TEMClient._default_timeout)

    def _set_unlimited_timeout(self):
        self.socket.setsockopt(zmq.SNDTIMEO, -1)
        self.socket.setsockopt(zmq.RCVTIMEO, -1)

    def _send_message(self, message):
        
        self.socket.connect(f"tcp://{self.host}:{self.port}")
        if self.verbose:
            print(f'[spring_green4]Sending: {message}[/spring_green4]')
        self.socket.send_string(message)
        reply = self.socket.recv_string()
        status, message = self._decode_reply(reply)
        if self.verbose:
            print(f'[dark_orange3]Received: {status}:{message}[/dark_orange3]')
        self.socket.disconnect(f"tcp://{self.host}:{self.port}")
        return status, message

    def _decode_reply(self, reply):
        if ':' in reply:
            status, message = reply.split(':')
        else:
            status = reply
            message = None
        return status, message

    def ping(self):
        status, message  = self._send_message("ping")
        if status == "OK" and message == "pong":
            return True
        else:   
            raise ValueError(f"Unexpected reply: {status}:{message}")
        

if __name__ == "__main__":
    c = TEMClient("localhost", 4599)
    c.ping()