# simple-tem

- Remote control of PyJEM using ZeroMQ REQ/REP
- Synchronous execution for all commands 
- Supports run_async = True for SetTiltXAngle 
- might be turned into a conda pkg once stable
- PyJEM API: https://pyjem.github.io/PyJEM/interface/PyJEM.TEM3.html


## usage

**Server**

Copy tem-server.py to the machine where PyJEM is installed

**Client**
Make sure the simple-tem folder is added to PYTHONPATH (or conda pkg installed)

```python
from simple_tem import TEMClient
c = TEMClient("temserver", 3535)

c.ping() #check connection
c.stage_position #read position
c.SetILs(21500, 24500)

#Waits for stage to reach target (Most of the time, PyJEM bug?)
c.SetTiltXAngle(0) 

#No wait
c.SetTiltXAngle(40, run_async = True)
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

## Implementation

ZeroMQ REQ/REP socket sending a request as a multi part message 
```
[command_name : string][arguments : json_encoded_string]
```

Reply as
```
[status_code : string][return_value : json_encoded_string]
```