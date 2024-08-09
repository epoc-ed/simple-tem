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

## Tests

**Using Python 3.5 Launch the tem server in dummy mode**
This is becaues the PyJEM env on the TEM PC is still Python 3.5
```bash
python tem-server.py -d
```

**From your normal env run the tests**
```bash
python -m pytest
```