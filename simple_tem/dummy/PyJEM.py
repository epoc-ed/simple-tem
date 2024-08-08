
class Stage3:
    def __init__(self):
        pass
    def GetPos(self):
        return [1.1, 1.2, 1.3, 1.4, 1.5]
    
    def GetStatus(self):
        return [0,0,0,0,0]
    
    def SetZRel(self, value):
        if not isinstance(value, float):
            raise ValueError("SetZReal needs a float")
        return
    
    def SetXRel(self, value):
        if not isinstance(value, float):
            raise ValueError("SetXReal needs a float")
        return
    
    def SetTXRel(self, value):
        if not isinstance(value, float):
            raise ValueError("SetTXReal needs a float")
        return
    
    def SetTiltXAngle(self, val):
        return
    
    def Getf1OverRateTxNum(self) -> int:
        return 0

    def Setf1OverRateTxNum(self, val):
        return

    def GetMovementValueMeasurementMethod(self):
        return 0
    
    def Stop(self):
        return
    
class EOS3:
    def __init__(self):
        pass

    def GetMagValue(self):
        return [15000, 'X', 'X15k']
    
    def GetFunctionMode(self):
        return [4, 'DIFF']
    
    def SelectFunctionMode(self, mode):
        if not isinstance(mode, int):
            raise ValueError
    
    def SetSelector(self, value):
        if not isinstance(value, int):
            raise ValueError
        
    def GetSpotSize(self):
        return 3

    def GetAlpha(self):
        return 4

class Lens3:
    def __init__(self):
        pass

    def SetILFocus(self, value):
        if not isinstance(value, int):
            raise ValueError
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
        pass

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
        return
    
    def GetBeamBlank(self):
        return 1
    
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