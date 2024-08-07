import zmq
from rich import print
import json

class TEMClient:
    _default_timeout = 1000 #1s

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.verbose = True

        self._set_default_timeout()
        print(f"endpoint: {self.host}:{self.port}")

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
        
    def exit(self):
        status, message  = self._send_message("exit")
        if status == "OK" and message == "Bye!":
            return True
        else:   
            raise ValueError(f"Unexpected reply: {status}:{message}")

    @property
    def stage_position(self):
        status, message  = self._send_message("GetStagePosition")
        if status == "OK":
            message = message.replace("'", '"')
            res = json.loads(message)
            return res
        else:   
            raise ValueError(f"Unexpected reply: {status}:{message}")
        
    def SetILFocus(self, value):
        status, message  = self._send_message(f"SetILFocus:{value}")
        if status == "OK":
            return message
        else:   
            raise ValueError(f"Unexpected reply: {status}:{message}")
        
    def SetILs(self, stig_x, stig_y):
        status, message  = self._send_message(f"SetILs:{stig_x},{stig_y}")
        if status == "OK":
            return message
        else:   
            raise ValueError(f"Unexpected reply: {status}:{message}")
        
    def SetZRel(self, val):
        status, message  = self._send_message(f"SetZRel:{val}")
        if status == "OK":
            return message
        else:   
            raise ValueError(f"Unexpected reply: {status}:{message}")
        
    def SetTXRel(self, val):
        status, message  = self._send_message(f"SetTXRel:{val}")
        if status == "OK":
            return message
        else:   
            raise ValueError(f"Unexpected reply: {status}:{message}")

    def GetMagValue(self):
        status, message = self._send_message('GetMagValue')
        if status == "OK":
            message = message.replace("'", '"')
            res = json.loads(message)
            return res
        else:   
            raise ValueError(f"Unexpected reply: {status}:{message}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("host")
    args = parser.parse_args()
    # c = TEMClient("temserver", 3535)
    c = TEMClient(args.host, 3535)
    c.ping()
    # print(c.stage_position)
