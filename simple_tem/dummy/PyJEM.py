
class Stage3:
    def __init__(self):
        pass
    def GetPos(self):
        return [1.1, 1.2, 1.3, 1.4, 1.5]
    
    def GetStatus(self):
        return 0
    
    def SetZRel(self, value):
        if not isinstance(value, float):
            raise ValueError("SetZReal needs a float")
        return
    
    def SetTXRel(self, value):
        if not isinstance(value, float):
            raise ValueError("SetTXReal needs a float")
        return
    
class EOS3:
    def __init__(self):
        pass

    def GetMagValue(self):
        return [15000, 'X', 'X15k']
    
    def GetFunctionMode(self):
        return 0

class Lens3:
    def __init__(self):
        pass

    def SetILFocus(self, value):
        if not isinstance(value, int):
            raise ValueError
        #TODO! check range
        pass 

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

class TEM3:
    def __init__(self):
        pass
    @staticmethod
    def HT3():
        return 0
    @staticmethod
    def Apt3():
        return 0
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