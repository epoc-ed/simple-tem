import zmq
import json
from rich import print
from datetime import datetime

class TEMClient:
    _default_timeout = 1000 #1s
    _ping_timeout = 1000 #1s
    encoding = 'ascii'

    def __init__(self, host, port = 3535, verbose = True):
        self.host = host
        self.port = port
        self.verbose = verbose
        print(f"TEMClient:endpoint: {self.host}:{self.port}")


    def _send_message(self, cmd, *args, timeout_ms = -1):
        
        cmd = cmd.encode(TEMClient.encoding)
        args = json.dumps(args).encode(TEMClient.encoding)
        if self.verbose:
            print(f'[spring_green4]{self._now()} - REQ: {cmd}, {args}[/spring_green4]')

        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.setsockopt(zmq.SNDTIMEO, timeout_ms)
        socket.setsockopt(zmq.RCVTIMEO, timeout_ms)
        socket.setsockopt(zmq.LINGER, 0)
        socket.connect(f"tcp://{self.host}:{self.port}")

        try:
            socket.send_multipart([cmd, args])
            reply = socket.recv_multipart()
            status, message = self._decode_reply(reply)
            if self.verbose:
                print(f'[dark_orange3]{self._now()} - REP: {status}:{message}[/dark_orange3]')
            self._check_error(status, message) #TODO! Add function
        
        except zmq.error.Again:
            raise TimeoutError(f"Timeout while waiting for reply from {self.host}:{self.port}")
        
        finally:
            socket.disconnect(f"tcp://{self.host}:{self.port}")
            context.destroy()
        
        return message

    def _decode_reply(self, reply):
        return (json.loads(r) for r in reply)
  
    def _check_error(self, status, message):
        if status != "OK":
            raise ValueError(f"Unexpected reply: {status}:{message}")
        
    def _now(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def ping(self, timeout_ms = None) -> bool:
        """
        Check if the server is alive and accepts commands
        Default is a 1s timeout
        """
        if timeout_ms is None:
            timeout_ms = TEMClient._ping_timeout
        
        try: 
            rep =  self._send_message("ping", timeout_ms=timeout_ms)
            return rep == "pong"
        except (TimeoutError):
            return False

    @property
    def is_alive(self):
        return self.ping()

    def sleep(self) -> None:
        self._send_message("sleep")

        
    def exit_server(self) -> None:
        """
        Exit the server
        """
        self._send_message("exit_server")

    def UnknownFunction(self):
        """
        Calls an unknown function on the server side. Testing only
        """
        return self._send_message("UnknownFunction")

    # --------------------- STAGE ---------------------
        
    def GetStagePosition(self):
        """
        Get motor position. it depends on the drive mode.
        (x : float, y : float, z : float, tiltx : float, tilty : float)
        """
        return self._send_message("GetStagePosition")
        
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
        return self._send_message('GetStageStatus')

    @property
    def stage_is_rotating(self):
        return self._send_message('GetStageStatus')[3] == 1

    def SetZRel(self, val : float) -> None:
        """
        Relative move along Z axis.
        Range:+-100000.0(nm)
        """
        self._send_message("SetZRel", val)
    
    def SetXRel(self, val : float) -> None:
        """
        Relative move along Z axis.
        Range:+-100000.0(nm)
        """
        self._send_message("SetXRel", val)

    def SetYRel(self, val : float) -> None:
        """
        Relative move along Z axis.
        Range:+-100000.0(nm)
        """
        self._send_message("SetYRel", val)

    def SetTXRel(self, val : float, run_async: bool = False, max_speed: bool = False) -> None:
        """
        Relative tilt around X axis.
        tilt-x relative value. range is +-90.00.0(degree)
        run_async: run the command asynchronously and return immediately
        max_speed: rotate at maximum speed, restore previous speed after rotation
        """
        self._send_message("SetTXRel", val, run_async, max_speed)

    def SetTiltXAngle(self, val, run_async = False, max_speed = False) -> None:
        """
        Set TiltX axis absolute value. range is +-90.00(degree)
        run_async: run the command asynchronously and return immediately
        max_speed: rotate at maximum speed, restore previous speed after rotation
        """
        self._send_message("SetTiltXAngle", val, run_async, max_speed)

    def GetTiltXAngle(self) -> float:
        """
        Get the  Tilt angle, alias for StagePos[3]
        """
        return self._send_message('GetStagePosition')[3]

    def Getf1OverRateTxNum(self):
        """
        Get drive frequency f1 of TiltX.
        0= 10(/sec), 1= 2(/sec), 2= 1(/sec), 3= 0.5(/sec), 4= 0.25(/sec), 5= 0.1(/sec)
        """
        return self._send_message("Getf1OverRateTxNum")

    def Setf1OverRateTxNum(self, val) -> None:
        """
        Set drive frequency f1 of TiltX.
        """
        self._send_message("Setf1OverRateTxNum", val)
        
    def GetMovementValueMeasurementMethod(self):
        """
        Get movement amount measurement method (for Z/Tx/Ty).
        method. 0= encoder, 1= potens
        """
        return self._send_message("GetMovementValueMeasurementMethod")

    def StopStage(self) -> None:
        """Stop all the drives."""
        self._send_message("StopStage")



    # END STAGE

    # ---------------------- EOS ----------------------

    def GetMagValue(self) -> list:
        """
        Get magnification or camera length or rocking angle.
        returns (value, unit, name)
        """
        return self._send_message('GetMagValue')

    def GetFunctionMode(self) -> list:
        """
        (index, name)
        [On TEM Observation] 0=MAG, 1=MAG2, 2= LowMAG, 3= SAMAG, 4= DIFF
        [On STEM Observation] 0= Align, 1= SM-LMAG, 2= SM-MAG, 3= AMAG, 4= uuDIFF, 5= Rocking
        """
        return self._send_message('GetFunctionMode')


    def SelectFunctionMode(self, mode : int) -> None:
        """
        [On TEM Observation] 0=MAG, 1=MAG2, 2= LowMAG, 3= SAMAG, 4= DIFF
        [On STEM Observation] 0= Align, 1= SM-LMAG, 2= SM-MAG, 3= AMAG, 4= uuDIFF, 5= Rocking
        """
        self._send_message("SelectFunctionMode", mode)

        
    def SetSelector(self, value : int) -> None:
        """
         (int) mag or camera length or rocking angle number value.
        """
        self._send_message("SetSelector", value)

    def GetSpotSize(self) -> int:
        """
        Get spot size number. 0-7
        """
        return self._send_message("GetSpotSize")

    def GetAlpha(self) -> int:
        """
        Get alpha number. 0-8
        """
        return self._send_message("GetAlpha")

    # END EOS
    # --------------------- LENS ---------------------

    def SetILFocus(self, value) -> None:
        """
        Set IL-focus value(without MAG link).
        IL-focus value.(0-65535)
        """
        self._send_message("SetILFocus", value)


    def GetCL3(self) -> int:
        """
        CL3 value(0-65535).
        """
        return self._send_message('GetCL3')

    def GetIL1(self) -> int:
        """
        IL1 value(0-65535).
        """
        return self._send_message('GetIL1')


    def GetIL3(self) -> int:
        """
        IL3 value(0-65535).
        """
        return self._send_message('GetIL3')

    def GetOLf(self) -> int:
        """
        GetOLf value(0-65535).
        """
        return self._send_message('GetOLf')

    
    def GetOLc(self) -> int:
        """
        GetOLc value(0-65535).
        """
        return self._send_message('GetOLc')
        

    # END LENS
    # ---------------------- DEF ----------------------


    def GetILs(self):
        """
        Get ILStig value. this returns I/O output value.
        (x : int, y : int) 0-65535
        """
        return self._send_message('GetILs')

        
    def SetILs(self, stig_x : int, stig_y : int):
        """
        Set ILStig value. The variable corresponds to I/O output value.
        (x_axis : int, y_axis : int) 0-65535
        """
        self._send_message("SetILs", stig_x, stig_y)
        
        
        
    def GetPLA(self):
        """
        Get PLAlign value. this returns I/O output value.
        (x : int, y : int) 0-65535
        """
        return self._send_message('GetPLA')

    def GetBeamBlank(self) -> int:
        """
        blanking status. 0=OFF, 1=ON
        """
        return self._send_message('GetBeamBlank')

    def SetBeamBlank(self, val) -> None:
        """
        blanking status. 0=OFF, 1=ON
        """
        self._send_message("SetBeamBlank", val)
    

    # END DEF
    # ---------------------- APT ----------------------     

    def GetAperatureSize(self, index):
        """
        index : int aperture kind. 
        1= CLA, 2= OLA, 3= HCA, 4= SAA, 5= ENTA, 6= EDS

        returns: Selected aperture’s hole number. 0= Open, 1-4= hole index
        """
        return self._send_message("GetAperatureSize", index)
