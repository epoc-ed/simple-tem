import pytest
from simple_tem import TEMClient

@pytest.fixture
def client():
    c = TEMClient('localhost')
    c.SetTiltXAngle(0, max_speed=True)
    c.Setf1OverRateTxNum(0)
    c.SetBeamBlank(0)
    return c