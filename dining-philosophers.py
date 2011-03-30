#!/usr/bin/python

def main(args):
    # Default values
    philosophers = 20
    duration = 5 # Seconds

    # Parse Arguments
    try:
        philosophers = int(args.pop(0))
        duration = float(args.pop(0))
    except: pass

if __name__ == '__main__':
    from sys import argv
    main(argv[1:])
