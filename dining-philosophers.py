#!/usr/bin/python

from philosophers import PhilosopherTable, Philosopher
from time import sleep

def main(args):
    # Default values
    seats = 20
    duration = 5 # Seconds

    # Parse Arguments
    try:
        seats = int(args.pop(0))
        duration = float(args.pop(0))
    except: pass

    # Set table
    # (Spam and rice for dinner)
    table = PhilosopherTable(seats)

    # Create list of philosophers
    # (Useful Python syntax called a
    #  'list comprehension')
    philosophers = [Philosopher(table, p)
                    for p in xrange(seats)]

    # Start philosophers
    for p in philosophers:
        p.start()

    sleep(duration)

    # Interrupt and join
    for p in philosophers:
        p.stop()

if __name__ == '__main__':
    from sys import argv
    main(argv[1:])
