# TEM server that listens to commands on a zeromq socket and
# executes them on a TEM3 object. The server is meant to be 
# standalone and can be run on the same machine as PyJEM
import argparse
from datetime import datetime
import json
import sys
import zmq

def now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class TEMServer:
    _IL1_DEFAULT = 21902
    STATUS_OK = 'OK'
    STATUS_ERROR = 'ERROR'
    encoding = 'ascii'
    _version_str = '2024.8.30' #TODO! Auto update

    def __init__(self, port):
        self.stage = TEM3.Stage3()
        self.lens = TEM3.Lens3()
        self.defl = TEM3.Def3()
        self.eos = TEM3.EOS3()
        self.apt = TEM3.Apt3()

        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        endpoint = "tcp://*:{}".format(port)
        print("{} - TEMServer binding to {} ".format(self._now(), endpoint))
        self.socket.bind(endpoint)

        #Find all commands
        self._commands = [it for it in dir(self) if callable(getattr(self, it)) and not it.startswith('_')]
    
    def _has_function(self, cmd):
        return cmd in self._commands

    def _now(self):
        return now()
    
    def ping(self):
        return "pong"

    def exit_server(self):
        return "Bye!"
    
    def version(self):
        return TEMServer._version_str
        
    # --------------------- STAGE ---------------------
    def GetStagePosition(self):
        return self.stage.GetPos()

    def GetStageStatus(self):
        return self.stage.GetStatus()

    def SetZRel(self, val : float):
        self.stage.SetZRel(val)

    def SetXRel(self, val : float):
        self.stage.SetXRel(val)

    def SetYRel(self, val : float):
        self.stage.SetYRel(val)

    def SetTXRel(self, val : float):
        self.stage.SetTXRel(val)

    def SetTiltXAngle(self, tilt : float):
        self.stage.SetTiltXAngle(tilt)

    def Getf1OverRateTxNum(self):
        return self.stage.Getf1OverRateTxNum()
    
    def Setf1OverRateTxNum(self, val : int):
        return self.stage.Setf1OverRateTxNum(val)

    def GetMovementValueMeasurementMethod(self):
        return self.stage.GetMovementValueMeasurementMethod()

    def StopStage(self):
        self.stage.Stop()

    # END STAGE _______________________________________
    # ---------------------- EOS ----------------------
    def GetMagValue(self):
        return self.eos.GetMagValue()
    
    def GetFunctionMode(self):
        return self.eos.GetFunctionMode()
    
    def SelectFunctionMode(self, mode):
        self.eos.SelectFunctionMode(mode)

    def SetSelector(self, value):
        self.eos.SetSelector(value)

    def GetSpotSize(self):
        return self.eos.GetSpotSize()

    def GetAlpha(self):
        return self.eos.GetAlpha()

    # END EOS__________________________________________
    # ---------------------- APT ----------------------
    
    def GetAperatureSize(self, index):
        return self.apt.GetSize(index)
    
    # END APT__________________________________________

    # --------------------- LENS ---------------------
    
    def SetILFocus(self, value):
        self.lens.SetILFocus(value)

    def GetCL3(self):
        return self.lens.GetCL3()
    
    def GetIL1(self):
        return self.lens.GetIL1()

    def GetIL3(self):
        return self.lens.GetIL3()

    def GetOLf(self):
        return self.lens.GetOLf()

    def GetOLc(self):
        return self.lens.GetOLc()
  
    # END LENS_________________________________________
    # --------------------- DEF ---------------------
    def GetILs(self):
        return self.defl.GetILs()

    def SetILs(self, stig_x, stig_y):
        self.defl.SetILs(stig_x, stig_y)

    def GetPLA(self):
        return self.defl.GetPLA()
    
    def GetBeamBlank(self):
        return self.defl.GetBeamBlank()

    def SetBeamBlank(self, blank):
        self.defl.SetBeamBlank(blank)

    # END DEF_________________________________________
    
    def _run(self):
        while True:
            msgs = self.socket.recv_multipart()
            
            #If we didn't get two messages something is really wrong so lets 
            #just exit and debug the caller
            if len(msgs) != 2:
                print("TEMServer got: {} messages. Should always be 2 -> EXIT".format(len(msgs)))
                sys.exit(1)

            cmd = msgs[0].decode(TEMServer.encoding)
            args = json.loads(msgs[1].decode(TEMServer.encoding))
            print("{} - REQ: {}, {}".format(self._now(), cmd, args))

            if self._has_function(cmd):
                # if the function in found we try to call it
                try:
                    res = getattr(self, cmd)(*args)
                    rc = TEMServer.STATUS_OK
                except Exception as e:
                    rc = TEMServer.STATUS_ERROR
                    res = "Exception occurred when calling: {}. Error message: {}".format(cmd, e)
            else:
                #Otherwise we return an error
                rc = TEMServer.STATUS_ERROR
                res = "Function: {} not implemented".format(cmd)

            rc = json.dumps(rc).encode(TEMServer.encoding)
            res = json.dumps(res).encode(TEMServer.encoding)
            
            # Reply to the client
            print("{} - REP: {}, {}".format(self._now(), rc, res))
            self.socket.send_multipart([rc, res])


            if cmd == 'exit_server':
                break


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dummy',
                    action='store_true')
    args = parser.parse_args()
    if args.dummy:
        from simple_tem.dummy.PyJEM import TEM3
    else:
        from PyJEM import TEM3


    s = TEMServer(3535)
    s._run()


