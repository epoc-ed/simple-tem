import pytest

from simple_tem import TEMClient

@pytest.fixture
def client():
    return TEMClient('localhost')


def test_ping_returns_true(client):
    res = client.ping()
    assert res


# --------------------- STAGE ---------------------

def test_GetStagePosition(client):
    pos = client.GetStagePosition()
    assert pos == [1.1, 1.2, 1.3, 1.4, 1.5]

def test_GetStageStatus(client):
    stat = client.GetStageStatus()
    assert stat == [0,0,0,0,0]

def test_SetZRel(client):
    client.SetZRel(400)

def test_SetXRel(client):
    client.SetXRel(34010)

def test_SetYRel(client):
    client.SetYRel(34020)

def test_SetTXRel(client):
    client.SetTXRel(400)

def test_SetTiltXAngle(client):
    client.SetTiltXAngle(33)

def test_Getf1OverRateTxNum(client):
    assert client.Getf1OverRateTxNum() == 0

def test_Setf1OverRateTxNum(client):
    client.Setf1OverRateTxNum(5)

def test_GetMovementValueMeasurementMethod(client):
    assert client.GetMovementValueMeasurementMethod() == 0

def test_StopStage(client):
    client.StopStage()
# ---------------------- EOS ----------------------

def test_GetMagValue(client):
    res = client.GetMagValue()
    assert res == [15000, 'X', 'X15k']

def test_GetFunctionMode(client):
    assert client.GetFunctionMode() == [4, 'DIFF']

def test_SelectFunctionMode(client):
    client.SelectFunctionMode(1)

def test_SetSelector(client):
    client.SetSelector(11)

def test_GetSpotSize(client):
    assert client.GetSpotSize() == 3

def test_GetAlpha(client):
    assert client.GetAlpha() == 4

# --------------------- LENS ---------------------


def test_SetILFocus(client):
    client.SetILFocus(32000)

def test_GetCL3(client):
    assert client.GetCL3() == 0xFF00

def test_GetIL1(client):
    assert client.GetIL1() == 0xFFF0

def test_GetIL3(client):
    assert client.GetIL3() == 1234

def test_GetOLf(client):
    assert client.GetOLf() == 12345

def test_GetOLc(client):
    assert client.GetOLc() == 2345


# ---------------------- DEF ----------------------

def test_GetILs(client):
    assert client.GetILs() == [21000,22000]

def test_SetILs(client):
    client.SetILs(24000, 25000)

def test_GetPLA(client):
    assert client.GetPLA() == [25000,26000]

def test_GetBeamBlank(client):
    assert client.GetBeamBlank() == 1

def test_SetBeamBlank(client):
    client.SetBeamBlank(0)

# ---------------------- APT ----------------------

def test_GetAperatureSize(client):
    assert client.GetAperatureSize(0) == 2
    assert client.GetAperatureSize(1) == 3

# ---------------------- GENERAL ----------------------
def test_UnknownFunctionRaisesException(client):
    with pytest.raises(Exception):
        client.UnknownFunction()