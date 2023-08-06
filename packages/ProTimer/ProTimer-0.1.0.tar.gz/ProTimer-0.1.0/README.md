# ProTimer
blocker to block programs until an event happens
# installation

Run the following to install:
```cmd
pip install ProTimer
```
### or
```cmd
python -m pip install ProTimer
```
if that didn't work, try replacing `pip` with `pip3`.
need help? my discord: [lab](https://discord.gg/vzEZnC7CM8)

# two test programs
> **Warning**
> the two programs may not start at the exact time
```python
import time
from ProTimer import timer
from ProTimer import system
timer = timer(10)
# this must be in one of the programs
timer.start() # start a timer
system.sleep() # block the program for timer(s)
for i in range(10):
	time.sleep(1)
	print(i,flush=True)
```
> **Warning** don't put timer Object in two programs at the same time
```python
import time
from ProTimer import system
system.sleep() # timer(10s) blocking
for i in range(10):
	time.sleep(1)
	print(i,flush=True)
```
> **Note** you must start the programs at the same time or start at close time


# system class

## sleep
wait until a time ends
```python
system.sleep()
```
## is_running
```python
if a process is running or not
"""
return a booling
if is running return True
else is not running return False
"""
# pids can be None
system.is_running(process.name,process.pids)
```
## run_until
wait until the process is finish
```python
# pids is None by default
system.run_until(process.name,process.pids)
```
## run_until_completed
wait until the process is finish with timeout
```python
# pids is None by default
# timeout is by (default is 10)
system.run_until_completed(process.name,process.pids,timeout=timeout)
```

#  timerquit
if the function took too long it raise KeyboardInterrupt
## exit_after
```python
@timerquit.exit_after(9)
def foo(bar):
    print ('hello {0}'.format(bar))
    time.sleep(10)
    return ("foo")
try:
	print(foo(bar="hello"))
except KeyboardInterrupt:
	pass
```