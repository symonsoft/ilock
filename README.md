# ilock v.1.0.3


## About

This is inter-process named lock library.
It provides only one class ILock with very simple interface.

Based on locking unique temporary files with [portalocker](https://github.com/WoLpH/portalocker).


## Installation

```sh
$ pip install ilock
```


## Examples

Here's a basic example:

```python
from ilock import ILock

with ILock('Unique lock name'):
    # The code should be run as a system-wide single instance
    ...
```

Example using timeout:

```python
from ilock import ILock, ILockException

try:
    with ILock('Unique lock name', timeout=15):
        # The code should be run as a system-wide single instance
        ...
except ILockException:
    # ILockException is raised when timeout was reached, but the lock wasn't acquired
    ...
```

Example using reentrant lock:

```python
from ilock import ILock, ILockException

lock = ILock('Unique lock name', reentrant=True)

def foo():
    with lock:
        # The code should be run as a system-wide single instance
        ...

with lock:
    # The code should be run as a system-wide single instance
    ...
    # Call foo() without blocking
    foo()
    ...
```


## License

BSD
