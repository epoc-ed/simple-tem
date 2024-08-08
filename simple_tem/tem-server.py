import sys
import zmq
from datetime import datetime
import argparse



class TEMServer:
    _IL1_DEFAULT = 21902
    #List of all commands that we can use
    #we check against this list before 
    #running anything
    _stage_commands = ['GetStagePosition',
                       'GetStageStatus', 
                       'SetZRel',
                       'SetTXRel',
                       'SetTiltXAngle']
    
    _eos_commands = ['GetMagValue',]

    _lens_commands = ['SetILFocus',
                      'GetCL3',
                      'GetIL1',
                      ]
    
    _def_commands = ['GetILs',
                     'SetILs', 
                     'GetPLA',
                     'GetBeamBlank',
                     'SetBeamBlank',
                     ]

    _commands = ['exit', 
                 'ping', 
                ]

    _commands += _stage_commands + _eos_commands + _lens_commands + _def_commands
    
    def __init__(self, port):

        self.stage = TEM3.Stage3()
        self.lens = TEM3.Lens3()
        self.defl = TEM3.Def3()
        self.eos = TEM3.EOS3()

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
    
    def GetMagValue(self):
        value = self.eos.GetMagValue()
        return "OK:{}".format(value)
    
    def SetILFocus(self, value):
        value = self._from_string("u2", value)
        print("Setting IL Focus to: {}".format(value))
        self.lens.SetILFocus(value)
        #TODO! Error checking
        return "OK:{}".format(value)
    
    def SetILs(self, stig_x, stig_y):
        stig_x = self._from_string("u2", stig_x)
        stig_y= self._from_string("u2", stig_y)
        self.defl.SetILs(stig_x, stig_y)
        return "OK:{},{}".format(stig_x, stig_y)

    def SetZRel(self, val : float):
        #TODO! range
        val = self._from_string("f", val)
        self.stage.SetZRel(val)
        return "OK:{}".format(val)
    
    def SetTXRel(self, val : float):
        #TODO! range
        val = self._from_string("f", val)
        self.stage.SetTXRel(val)
        return "OK:{}".format(val)

    def GetCL3(self):
        #int 0-0xFFFF
        val = self.lens.GetCL3()
        return "OK:{}".format(val)
    
    def GetIL1(self):
        #int 0-0xFFFF
        val = self.lens.GetIL1()
        return "OK:{}".format(val)
    
    def GetILs(self):
        #(int,int) 0-0xFFFF
        val = self.defl.GetILs()
        return "OK:{}".format(val)
    
    def GetPLA(self):
        #(int,int) 0-0xFFFF
        val = self.defl.GetPLA()
        return "OK:{}".format(val)
    
    def SetBeamBlank(self, blank):
        #blanking status
        #0 - OFF
        #1 - ON
        value = self._from_string("u2", blank) #TODO! force 0,1
        self.defl.SetBeamBlank(value)
        return "OK:{}".format(value)
    
    def GetBeamBlank(self):
        #(int,int) 0-0xFFFF
        val = self.defl.GetBeamBlank()
        return "OK:{}".format(val)

    def SetTiltXAngle(self, tilt : float):
        value = self._from_string("f", tilt) 
        self.stage.SetTiltXAngle(value)
        return "OK:{}".format(value)
    
    def GetStageStatus(self):
        stat = self.stage.GetStatus()
        return "OK:{}".format(stat)
    
    def exit(self):
        """special case since we are exiting"""
        self.socket.send_string("OK:Bye!")
        sys.exit()

    def _from_string(self, fmt, s):
        #TODO! factor out? 
        if fmt == "u2":
            value = int(s)
            if value < 0 or value > 0xFFFF:
                raise ValueError("Integer out of range")
            return value
        elif fmt == "f":
            value = float(s)
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
