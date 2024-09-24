import pytest
from simple_tem import TEMClient
import time

@pytest.fixture
def client():
    c = TEMClient('localhost')
    c.Setf1OverRateTxNum(0)
    c.SetTiltXAngle(0)
    while c.stage_is_rotating:
        time.sleep(0.1)

    c.SetBeamBlank(0)
    return c