import argparse
import logging
import time

from atomneighbors import NeighborFinder

parser = argparse.ArgumentParser()
parser.add_argument("--path", "-p", type=str, help="Path of the input coordinates")
parser.add_argument("--radius", "-r", help="Search radius")
parser.add_argument("--nrandom", "-n", help="Generate n random nodes")
parser.add_argument("--debug", help="Turn on debug mode", action="store_true")
parser.add_argument("--quiet", "-q", help="Don't print results to stdout", action="store_true")
parser.add_argument("--time", "-t", help="Performance profiling mode", action="store_true")
args = parser.parse_args()

def run():
    if args.quiet:
        loglevel = logging.WARNING
    elif args.debug or args.time:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO
    logging.basicConfig(level=loglevel)
    kwargs = {'radius': args.radius}
    if args.path:
        kwargs['path'] = args.path
    elif args.nrandom:
        kwargs['nrand'] = args.nrandom
    if args.time:
        time_profile(**kwargs)
    else:
        neighbors = NeighborFinder(**kwargs)
        neighbors.find_all()

def time_profile(**kwargs):
    start = time.time()
    neighbors = NeighborFinder(**kwargs)
    init_time = time.time()
    logging.debug(f"Init time: {init_time - start}")
    neighbors.find_all()
    end_time = time.time()
    logging.debug(f"Search time: {end_time - init_time}")
    logging.debug(f"Total time: {end_time - start}")

if __name__ == "__main__":
    run()
