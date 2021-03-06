"""
This modules includes the code related to the
philosophers, including the threads, and the table,
which acts as a monitor for synchronization.
"""

from threading import Thread, RLock, Condition

class State(object):
    """
    Represents the state of a philosopher
    """
    def __init__(self, string):
        self.string = string

    def __str__(self):
        return self.string

THINKING = State('T')
HUNGRY   = State('H')
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
            # The 'with' syntax automagically
            # takes care of acquiring and
            # releasing the lock in a try-finally
            # around the specified block
            with self.monitor_lock:
                return f(self, *args, **kw)
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
        """Index to the left of i"""
        return (i + self.seats - 1) % self.seats

    def right(self, i):
        """Index to the right of i"""
        return (i + 1) % self.seats

    def set_state(self, i, state):
        """Sets, checks, and prints new state"""
        self.states[i] = state
        self.sanity_check()
        print self

    def sanity_check(self):
        """Make sure we're not in an illegal state"""
        for i in xrange(self.seats):
            ieat = self.states[i] == EATING
            leat = self.states[self.left(i)] == EATING
            reat = self.states[self.right(i)] == EATING
            assert(not(ieat and (leat or reat)))

    def __str__(self):
        strs = []
        for p in xrange(self.seats):
            pstate = self.states[p]
            if pstate == EATING:
                strs += ['|%s| ' % pstate]
            else:
                if self.states[self.right(p)] == EATING:
                    strs += [' %s  ' % pstate]
                else:
                    strs += [' %s |' % pstate]

        return ''.join(strs)

class Philosopher(Thread):
    """
    The actual philosopher object, which is its own
    thread and interacts with a given table
    """
    def __init__(self, table, seat):
        super(Philosopher, self).__init__()
        self.table = table
        self.seat = seat

        # Lock and variable for interrupt
        self.ilock = RLock()
        self.interrupted = False

    # Override 'run()' method
    def run(self):
        """Called when the thread is started"""
        while True:
            # Access 'interrupted' with mutual exclusion
            with self.ilock:
                if self.interrupted: break

            self.think()
            self.table.pickup(self.seat)
            self.eat()
            self.table.putdown(self.seat)

    def think(self): random_sleep(0.50)
    def eat(self):   random_sleep(0.25)

    def interrupt(self):
        """
        Interrupts the thread associated
        with this philosopher
        """
        # Access 'interrupted' with mutual exclusion
        with self.ilock:
            self.interrupted = True

def random_sleep(max_time):
    """
    Sleeps for random time,
    up to max time in seconds
    """
    from time import sleep
    from random import random
    sleep(max_time*random())
