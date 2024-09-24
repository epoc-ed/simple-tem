
import pytest
import time

# --------------------- STAGE ---------------------

def test_GetStagePosition(client):
    #ensure that the rotatioten angle is 1.4
    client.SetTiltXAngle(1.4)
    while client.stage_is_rotating:
        time.sleep(0.1)
    pos = client.GetStagePosition()
    assert pos == pytest.approx([1.1, 1.2, 1.3, 1.4, 1.5])

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
    client.SetTXRel(5)
    while client.stage_is_rotating:
        time.sleep(0.1)
    assert client.GetStagePosition()[3] == pytest.approx(5)
    client.SetTXRel(-3.5)
    while client.stage_is_rotating:
        time.sleep(0.1)
    assert client.GetStagePosition()[3] == pytest.approx(1.5)


def test_SetTiltXAngle_async(client):
    # always runs async
    t0 = time.perf_counter()
    client.SetTiltXAngle(20)
    t1 = time.perf_counter()
    assert t1-t0 < .3

    #wait until the stage actually stopped
    while client.GetStageStatus()[3]:
        time.sleep(0.1)

def test_GetTiltXAngle(client):
    assert client.GetTiltXAngle() == pytest.approx(0)

def test_Getf1OverRateTxNum(client):
    assert client.Getf1OverRateTxNum() == 0

def test_Setf1OverRateTxNum(client):
    client.Setf1OverRateTxNum(1)
    assert client.Getf1OverRateTxNum() == 1

def test_GetMovementValueMeasurementMethod(client):
    assert client.GetMovementValueMeasurementMethod() == 0

def test_StopStage(client):
    client.SetTiltXAngle(30)
    time.sleep(0.5)
    client.StopStage()
    time.sleep(0.5)
    assert client.GetStageStatus()[3] == 0
    assert client.GetStagePosition()[3] < 10