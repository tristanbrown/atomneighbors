"""Utility functions"""
import itertools
import numpy as np

def hypercube3d():
    first_shell = np.array(list(itertools.product([-1, 0, 1], repeat=3)))
    shifts = [[1, 0, 0], [0, 1, 0], [0, 0, 1],
             [-1, 0, 0], [0, -1, 0], [0, 0, -1]]
    all_shells = [first_shell + np.array(shift) for shift in shifts] + [first_shell]
    all_shells = np.concatenate(all_shells, axis=0)
    all_shells = np.unique(all_shells, axis=0)
    return all_shells
