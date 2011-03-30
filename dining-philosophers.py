#!/usr/bin/python

from philosophers import PhilosopherTable

def main(args):
    # Default values
    seats = 20
    duration = 5 # Seconds

    # Parse Arguments
    try:
        seats = int(args.pop(0))
        duration = float(args.pop(0))
    except: pass

    table = PhilosopherTable(seats)
    table.pickup(0)
    table.putdown(0)

if __name__ == '__main__':
    from sys import argv
    main(argv[1:])
