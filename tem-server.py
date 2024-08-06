import zmq
from datetime import datetime
class TEMServer:

    #List of all commands that we can use
    _commands = ['ping']
    
    def __init__(self, port):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)

        endpoint = f"tcp://*:{port}"
        print(f"TEMServer binding to {endpoint} ")
        self.socket.bind(endpoint)

    def _decode(self, message):
        """
        Decode the message into a command and arguments
        """
        if ':' in message:
            cmd, args = message.split(':')
            if ',' in args:
                args = args.split(',')
            else:
                args = [args]
        else:
            cmd = message
            args = []
        
        return cmd, args
    
    def _has_function(self, cmd):
        return cmd in self._commands

    def _now(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def ping(self):
        return "OK:pong"


    def run(self):
        while True:
            #  Wait for next request from client
            message = self.socket.recv_string()
            cmd, args = self._decode(message)
            print(f'{self._now()} - Decoded to: {cmd}, {args}')

            #Call the right function with the arguments
            res = getattr(self, cmd)(*args)
            
            #Reply to the client
            print(f"{self._now()} - Sending reply: {res}")
            self.socket.send_string(res)

if __name__ == "__main__":
    s = TEMServer(4599)
    s.run()
