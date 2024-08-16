
import time


#Needed to synchronize values between processes
import redis

class PyJEM_DummyConf:
    redis_port = 5454

def redis_init():
    r = redis.Redis(port = PyJEM_DummyConf.redis_port)
    if r.get("x_angle") is None:
        r.set("x_angle", 0)
    if r.get("f1OverRateTxNum") is None:
        r.set("f1OverRateTxNum", 0)
    if r.get("x_is_rotating") is None:
        r.set("x_is_rotating", 0)
    if r.get("beam_blank") is None:
        r.set("beam_blank", 0)
    if r.get("stop_stage") is None:
        r.set("stop_stage", 0)
redis_init()


class Stage3:
    _degrees_per_second = [10, 2, 1, 0.5, 0.25, 0.1]

    def __init__(self):
        self.redis = redis.Redis(port = PyJEM_DummyConf.redis_port)

    def _rotate(self, target_angle):
        current_angle = float(self.redis.get("x_angle"))
        if current_angle == target_angle:
            return
        else:
            n_steps = 50
            step = (target_angle-current_angle) / n_steps
            self.redis.set("stop_stage", 0) #potential race condition
            self.redis.set("x_is_rotating", 1)
            for i in range(n_steps):
                self.redis.incrbyfloat("x_angle", step)
                print("rotate: incremented x_angle by ", step)
                #Read speed each time to account for changes
                t = abs(step/self._degrees_per_second[self.Getf1OverRateTxNum()])
                time.sleep(t)
                if int(self.redis.get("stop_stage")):
                    self.redis.set("stop_stage", 0)
                    print("rotate: stage stopped")
                    break
            self.redis.set("x_is_rotating", 0)

    def GetPos(self):
        return [1.1, 1.2, 1.3, float(self.redis.get('x_angle')), 1.5]
    
    def GetStatus(self):
        return [0,0,0,int(self.redis.get("x_is_rotating")),0]
    
    def SetZRel(self, value):
        if not isinstance(value, (float, int)):
            raise ValueError("SetZReal needs a float or int")
        return
    
    def SetXRel(self, value):
        if not isinstance(value, (float, int)):
            raise ValueError("SetXReal needs a float or int")
        return

    def SetYRel(self, value):
        if not isinstance(value, (float, int)):
            raise ValueError("SetYReal needs a float or int")
        return
    
    def SetTXRel(self, value):
        if not isinstance(value, (float, int)):
            raise ValueError("SetTXReal needs a float or int")
        current_angle = float(self.redis.get("x_angle"))
        self._rotate(current_angle + value)
    
    def SetTiltXAngle(self, val):
        #TODO! deal with concurrent access
        self._rotate(val)
    
    def Getf1OverRateTxNum(self) -> int:
        #0= 10(/sec), 1= 2(/sec), 2= 1(/sec), 3= 0.5(/sec), 4= 0.25(/sec), 5= 0.1(/sec)
        return int(self.redis.get("f1OverRateTxNum"))

    def Setf1OverRateTxNum(self, val):
        #0= 10(/sec), 1= 2(/sec), 2= 1(/sec), 3= 0.5(/sec), 4= 0.25(/sec), 5= 0.1(/sec)
        self.redis.set("f1OverRateTxNum", val)

    def GetMovementValueMeasurementMethod(self):
        return 0
    
    def Stop(self):
        if int(self.redis.get("x_is_rotating")):
            self.redis.set("stop_stage", 1)
    
    
    
class EOS3:
    def __init__(self):
        pass

    def GetMagValue(self):
        return [15000, 'X', 'X15k']
    
    def GetFunctionMode(self):
        return [4, 'DIFF']
    
    def SelectFunctionMode(self, mode):
        if not isinstance(mode, int):
            raise ValueError("SelectFunctionMode needs an int")
    
    def SetSelector(self, value):
        if not isinstance(value, int):
            raise ValueError("SetSelector needs an int")
        
    def GetSpotSize(self):
        return 3

    def GetAlpha(self):
        return 4

class Lens3:
    def __init__(self):
        pass

    def SetILFocus(self, value):
        if not isinstance(value, int):
            raise ValueError("SetILFocus needs int")
        #TODO! check range
        pass 

    def GetCL3(self):
        return 0xFF00
    
    def GetIL1(self):
        return 0xFFF0

    def GetIL3(self):
        return 1234
    
    def GetOLf(self):
        return 12345
    
    def GetOLc(self):
        return 2345
    


class Def3:
    def __init__(self):
        self.redis = redis.Redis(port = PyJEM_DummyConf.redis_port)

    def SetILs(self, stig_x, stig_y):
        if not isinstance(stig_x, int):
            raise ValueError
        if not isinstance(stig_y, int):
            raise ValueError
        #TODO! check range
        pass 

    def GetILs(self) -> list:
        return [21000,22000]
    
    def GetPLA(self) -> list:
        return [25000,26000]

    def SetBeamBlank(self, val):
        if not isinstance(val, int):
            raise ValueError
        self.redis.set("beam_blank", val)
    
    def GetBeamBlank(self):
        return int(self.redis.get("beam_blank"))
    
class Apt3:
    def __init__(self):
        pass

    def GetSize(self, index):
        if index == 0:
            return 2
        else:
            return 3


class TEM3:
    def __init__(self):
        pass
    @staticmethod
    def HT3():
        return 0
    @staticmethod
    def Apt3():
        return Apt3()
    @staticmethod
    def Stage3():
        return Stage3()
    @staticmethod
    def EOS3():
        return EOS3()
    @staticmethod
    def Def3():
        return Def3()
    @staticmethod
    def Lens3():
        return Lens3()