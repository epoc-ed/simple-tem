import sys
import zmq
from datetime import datetime
import argparse



class TEMServer:
    _IL1_DEFAULT = 21902
    #List of all commands that we can use
    _commands = ['ping', 'GetStagePos', 'SetILFocus', 'SetILs']
    
    def __init__(self, port):

        self.stage = TEM3.Stage3()
        self.lens = TEM3.Lens3()
        self.defl = TEM3.Def3()

        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)

        # endpoint = f"tcp://*:{port}"
        endpoint = "tcp://*:{}".format(port)
        print("TEMServer binding to {} ".format(endpoint))
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

    def GetStagePosition(self):
        pos = self.stage.GetPos()
        return "OK:{}".format(pos)
    
    def SetILFocus(self, value):
        value = self._from_string("u2", value)
        print("Setting IL Focus to: {}".format(value))
        self.lens.SetILFocus(value)
        #TODO! Error checking
        return "OK:{}".format(value)
    
    def SetILs(self, stig_x, stig_y):
        #Decode
        # assert len(value) == 2
        stig_x = self._from_string("u2", stig_x)
        stig_y= self._from_string("u2", stig_y)
        self.defl.SetILs(stig_x, stig_y)

        return "OK:{},{}".format(stig_x, stig_y)
    
    def exit(self):
        """special case since we are exiting"""
        self.socket.send_string("OK:Bye!")
        sys.exit()

    def _from_string(self, fmt, s):
        if fmt == "u2":
            value = int(s)
            if value < 0 or value > 0xFFFF:
                raise ValueError("Integer out of range")
            return value

        else:
            raise NotImplementedError("Conversion not implemented for: {}".format(fmt))

    
    
    def run(self):
        while True:
            #Wait for next request from client
            message = self.socket.recv_string()
            cmd, args = self._decode(message)
            print('{} - Decoded to: {}, {}'.format(self._now(), cmd, args))

            #If the command was not found return an error
            if not self._has_function(cmd):
                self.socket.send_string("ERROR:Unknown command")
                continue

            #Call the right function with the arguments
            res = getattr(self, cmd)(*args)
            
            #Reply to the client
            print("{} - Sending reply: {}".format(self._now(), res))
            self.socket.send_string(res)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dummy',
                    action='store_true')
    args = parser.parse_args()
    if args.dummy:
        from dummy.PyJEM import TEM3
    else:
        from PyJEM import TEM3
    s = TEMServer(3535)
    s.run()
