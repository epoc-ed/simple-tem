import zmq
from rich import print
import json

class TEMClient:
    _default_timeout = 1000 #1s

    def __init__(self, host, port = 3535):
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
        """
        Check if the server is alive, returns True or throws
        """
        status, message  = self._send_message("ping")
        if status == "OK" and message == "pong":
            return True
        else:   
            raise ValueError(f"Unexpected reply: {status}:{message}")
        
    def exit(self):
        """
        Exit the server
        """
        status, message  = self._send_message("exit")
        if status == "OK" and message == "Bye!":
            return True
        else:   
            raise ValueError(f"Unexpected reply: {status}:{message}")

    # --------------------- STAGE ---------------------
        
    def GetStagePosition(self):
        """
        Get motor position. it depends on the drive mode.
        (x : float, y : float, z : float, tiltx : float, tilty : float)
        """
        status, message  = self._send_message("GetStagePosition")
        if status == "OK":
            message = message.replace("'", '"')
            res = json.loads(message)
            return res
        else:   
            raise ValueError(f"Unexpected reply: {status}:{message}")
        
    @property
    def stage_position(self):
        return self.GetStagePosition()

    def GetStageStatus(self) -> list:
        """
        Get stage driving status. 
        0= Rest, 1= Moving, 2= Hardware limiter error
        (x : int, y : int, z : int, tiltx : int, tilty : int). 
        """
        # 
        status, message = self._send_message('GetStageStatus')
        if status == "OK":
            message = message.replace("'", '"')
            res = json.loads(message)
            return res
        else:   
            raise ValueError(f"Unexpected reply: {status}:{message}")  

    

    def SetZRel(self, val : float):
        """
        Relative move along Z axis.
        Range:+-100000.0(nm)
        """
        status, message  = self._send_message(f"SetZRel:{val}")
        if status == "OK":
            return message
        else:   
            raise ValueError(f"Unexpected reply: {status}:{message}")
        
    def SetTXRel(self, val : float):
        """
        Relative tilt around X axis.
        tilt-x relative value. range is +-90.00.0(degree)
        """
        status, message  = self._send_message(f"SetTXRel:{val}")
        if status == "OK":
            return message
        else:   
            raise ValueError(f"Unexpected reply: {status}:{message}")

    def SetTiltXAngle(self, val):
        """
        Set TiltX axis absolute value. range is +-90.00(degree)
        """
        status, message  = self._send_message(f"SetTiltXAngle:{val}")
        if status == "OK":
            return message
        else:   
            raise ValueError(f"Unexpected reply: {status}:{message}")

    # END STAGE

    # ---------------------- EOS ----------------------

    def GetMagValue(self) -> list:
        """
        Get magnification or camera length or rocking angle.
        returns (value, unit, name)
        """
        status, message = self._send_message('GetMagValue')
        if status == "OK":
            message = message.replace("'", '"')
            res = json.loads(message)
            return res
        else:   
            raise ValueError(f"Unexpected reply: {status}:{message}")
        
    # END EOS
    # --------------------- LENS ---------------------

    def SetILFocus(self, value):
        """
        Set IL-focus value(without MAG link).
        IL-focus value.(0-65535)
        """
        status, message  = self._send_message(f"SetILFocus:{value}")
        if status == "OK":
            return message
        else:   
            raise ValueError(f"Unexpected reply: {status}:{message}")

    def GetCL3(self) -> int:
        """
        CL3 value(0-65535).
        """
        status, message = self._send_message('GetCL3')
        if status == "OK":
            val = int(message)
            return val
        else:   
            raise ValueError(f"Unexpected reply: {status}:{message}")

    def GetIL1(self) -> int:
        """
        IL1 value(0-65535).
        """
        status, message = self._send_message('GetIL1')
        if status == "OK":
            val = int(message)
            return val
        else:   
            raise ValueError(f"Unexpected reply: {status}:{message}")

    # END LENS
    # ---------------------- DEF ----------------------


    def GetILs(self):
        """
        Get ILStig value. this returns I/O output value.
        (x : int, y : int) 0-65535
        """
        status, message = self._send_message('GetILs')
        if status == "OK":
            message = message.replace("'", '"')
            res = json.loads(message)
            return res
        else:   
            raise ValueError(f"Unexpected reply: {status}:{message}")
        
    def SetILs(self, stig_x : int, stig_y : int):
        """
        Set ILStig value. The variable corresponds to I/O output value.
        (x_axis : int, y_axis : int) 0-65535
        """
        status, message  = self._send_message(f"SetILs:{stig_x},{stig_y}")
        if status == "OK":
            return message
        else:   
            raise ValueError(f"Unexpected reply: {status}:{message}")
        
        
    def GetPLA(self):
        """
        Get PLAlign value. this returns I/O output value.
        (x : int, y : int) 0-65535
        """
        status, message = self._send_message('GetPLA')
        if status == "OK":
            message = message.replace("'", '"')
            res = json.loads(message)
            return res
        else:   
            raise ValueError(f"Unexpected reply: {status}:{message}")

    def GetBeamBlank(self) -> int:
        """
        blanking status. 0=OFF, 1=ON
        """
        status, message = self._send_message('GetBeamBlank')
        if status == "OK":
            val = int(message)
            return val
        else:   
            raise ValueError(f"Unexpected reply: {status}:{message}")

    def SetBeamBlank(self, val):
        """
        blanking status. 0=OFF, 1=ON
        """
        status, message  = self._send_message(f"SetBeamBlank:{val}")
        if status == "OK":
            return message
        else:   
            raise ValueError(f"Unexpected reply: {status}:{message}")
        
def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("host")
    parser.add_argument("-p", "--port", default = 3535)
    args = parser.parse_args()
    c = TEMClient(args.host, args.port)
    c.ping()

if __name__ == "__main__":
    main()

