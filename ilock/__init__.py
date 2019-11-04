import errno
import os
import sys
from hashlib import sha256
from tempfile import gettempdir
from time import time, sleep

import portalocker


class ILockException(Exception):
    pass


class ILock(object):
    def __init__(self, name, timeout=None, check_interval=0.25, reentrant=False, lock_directory=None):
        self._timeout = timeout if timeout is not None else 10 ** 8
        self._check_interval = check_interval

        lock_directory = gettempdir() if lock_directory is None else lock_directory
        unique_token = sha256(name.encode()).hexdigest()
        self._filepath = os.path.join(lock_directory, 'ilock-' + unique_token + '.lock')

        self._reentrant = reentrant

        self._enter_count = 0

    def __enter__(self):
        if self._enter_count > 0:
            if self._reentrant:
                self._enter_count += 1
                return self
            raise ILockException('Trying re-enter a non-reentrant lock')

        current_time = call_time = time()
        while call_time + self._timeout >= current_time:
            self._lockfile = open(self._filepath, 'w')
            try:
                portalocker.lock(self._lockfile, portalocker.constants.LOCK_NB | portalocker.constants.LOCK_EX)
                self._enter_count = 1
                return self
            except portalocker.exceptions.LockException:
                pass

            current_time = time()
            check_interval = self._check_interval if self._timeout > self._check_interval else self._timeout
            sleep(check_interval)

        raise ILockException('Timeout was reached')

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._enter_count -= 1

        if self._enter_count > 0:
            return

        if sys.platform.startswith('linux'):
            # In Linux you can delete a locked file
            os.unlink(self._filepath)

        self._lockfile.close()

        if sys.platform == 'win32':
            # In Windows you need to unlock a file before deletion
            try:
                os.remove(self._filepath)
            except WindowsError as e:
                # Mute exception in case an access was already acquired (EACCES)
                #  and in more rare case when it was even already released and file was deleted (ENOENT)
                if e.errno not in [errno.EACCES, errno.ENOENT]:
                    raise
