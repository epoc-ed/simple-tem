# simple-tem

- Single threaded TEM client based on zmq REQ/REP
- might be turned into a conda pkg once stable


## usage

**Server**

Copy tem-server.py to the machine where
PyJEM is installed

**Client**
```python
from simple_tem import TEMClient
c = TEMClient("temserver", 3535)

c.ping() #check connection
c.stage_position #read position
c.SetILs(21500, 24500)
...
```