# simple-tem

- Remote control of PyJEM using ZeroMQ REQ/REP
- Synchronous execution for all commands 
- Supports run_async = True for SetTiltXAngle 
- might be turned into a conda pkg once stable
- PyJEM API: https://pyjem.github.io/PyJEM/interface/PyJEM.TEM3.html


## Usage

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


c.SetTiltXAngle(35) 

...

# Check if we can talk to the sever before issuing a command
if c.is_alive:
    c.Sec.SetTiltXAngle(40)
else:
    raise SomeKindOfException


#Waiting for a rotation to finish
c.SetTiltXAngle(10)
c.wait_until_rotate_starts() #default timeout of 2s
while c.is_rotating:
    # some checks? 

#stage is now stopped verify angle 
a = c.GetTiltXAngle()

```

## Error handling

```python
#Check, with a 1s timeout, if the server is responding -> True/False
>>> c.is_alive 
True

#Normal calls have a timeout of 5s and then raises a TimeoutError
>>> c.GetStagePosition()
TimeoutError: Timeout while waiting for reply from sjsjs:3535

#Each call to PyJEM could fail
>>> c.Getf1OverRateTxNum()
RuntimeError: Function execution error. function: Stage3::Getf1OverRateTxNum, code : 20483
```

In some functions three  automatic retries with a 0.1s sleep is implemented
 - c.is_rotating

 But mostly the caller is responsible to handle the exceptions.

## Tests

**Start a local redis instance on port 5454**

This is used to hold values that we pretend to send to the microscope

```bash
redis-server --port 5454
```

**Using Python 3.5 Launch the tem server in dummy mode**
This is becaues the PyJEM env on the TEM PC is still Python 3.5. Of course if you want to test functtionallity without verifying python 3.5 compatibility you can use a later version of python.

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