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

def test_SetTXRel(client):
    client.SetTXRel(400)

def test_SetTiltXAngle(client):
    client.SetTiltXAngle(33)
# ---------------------- EOS ----------------------

def test_GetMagValue(client):
    res = client.GetMagValue()
    assert res == [15000, 'X', 'X15k']

# --------------------- LENS ---------------------


def test_SetILFocus(client):
    client.SetILFocus(32000)

def test_GetCL3(client):
    assert client.GetCL3() == 0xFF00

def test_GetIL1(client):
    assert client.GetIL1() == 0xFFF0


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