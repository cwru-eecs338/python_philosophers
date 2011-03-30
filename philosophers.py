"""
This modules includes the code related to the
philosophers, including the threads, and the table,
which acts as a monitor for synchronization.
"""

from threading import RLock, Condition

class State(object):
    """
    Represents the state of a philosopher
    """
    def __init__(self, string):
        self.string = string

    def __str__(self):
        return self.string

HUNGRY   = State('H')
THINKING = State('T')
EATING   = State('E')

class PhilosopherTable(object):
    """
    Acts a a monitor for synchronizing
    the eating of various philosophers.
    """
    def __init__(self, seats):
        self.monitor_lock = RLock()
        self.seats = seats
        self.states = {}
        self.conditions = {}
        for i in xrange(seats):
            self.states[i] = THINKING
            # Conditions variables must be initialized
            # with the lock corresponding to the monitor
            self.conditions[i] = Condition(self.monitor_lock)

    def synchronized(f):
        """
        This defines a 'decorator' which wraps the
        decorated function call with acquiring and
        releasing the lock associated with the
        monitor instance.
        """
        def wrapper(self, *args, **kw):
            self.monitor_lock.acquire()
            try:
                return f(self, *args, **kw)
            finally:
                self.monitor_lock.release()
        return wrapper

    @synchronized
    def pickup(self, i):
        pass

    @synchronized
    def putdown(self, i):
        pass

    @synchronized
    def _test(self, i):
        pass
