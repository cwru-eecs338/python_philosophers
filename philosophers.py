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
        self.set_state(i, HUNGRY)
        self.test(i)
        if self.states[i] != EATING:
            self.conditions[i].wait()

    @synchronized
    def putdown(self, i):
        self.set_state(i, THINKING)
        self.test(self.right(i))
        self.test(self.left(i))

    @synchronized
    def test(self, i):
        if (self.states[self.left(i)] != EATING
            and self.states[self.right(i)] != EATING
            and self.states[i] == HUNGRY):
            self.set_state(i, EATING)
            self.conditions[i].notify()

    def left(self, i):
        return (i + self.seats - 1) % self.seats

    def right(self, i):
        return (i + 1) % self.seats

    def set_state(self, i, state):
        self.states[i] = state
        # TODO Check
        print self

    def __str__(self):
        strs = []
        for p in xrange(self.seats):
            pstate = self.states[p]
            if pstate == EATING:
                strs += ['|%(pstate)s| ' % locals()]
            else:
                if self.states[self.right(p)] == EATING:
                    strs += [' %(pstate)s  ' % locals()]
                else:
                    strs += [' %(pstate)s |' % locals()]

        return ''.join(strs)
