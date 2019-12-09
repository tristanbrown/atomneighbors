"""Contains the class for finding the nearest neighbors."""
import logging

import numpy as np
import pandas as pd

from atomneighbors import util

class NeighborFinder():
    def __init__(self, path=None, radius=1, nrand=None):
        self.r = float(radius)
        self.gridsize = self.r / np.sqrt(3)
        self.hypercube = util.hypercube3d()
        if path:
            self.hash_table = self.load_inputs(path)
        elif nrand:
            self.hash_table = self.rand_nodes(int(nrand))
        self.candidates = None

    def load_inputs(self, path):
        """Load the coordinates defining the node space."""
        logging.debug(f"Loading neighbor radius search from {path}")
        data = pd.read_csv(path, skipinitialspace=True).set_index('ID')
        data['buckets'] = self._hash(data)
        return data

    def rand_nodes(self, n):
        """Generate n random nodes."""
        if n > 10000:
            raise ValueError(f"Too many nodes: {n}")
        data = pd.DataFrame(np.random.uniform(-10**7, 10**7, size=(n, 3)), columns=list('xyz'))
        data.index = data.index.rename('ID') + 1
        data['buckets'] = self._hash(data)
        return data

    def _hash(self, coords):
        """Hash the coordinates into buckets."""
        bucketed = (coords/self.gridsize).astype('int')
        return list(zip(bucketed['x'], bucketed['y'], bucketed['z']))

    def find_all(self):
        """Find all neighbors within the given radius for every node."""
        buckets = self.hash_table['buckets'].unique()
        self.candidates = {bucket: self.find_candidates(bucket) for bucket in buckets}
        result = self.hash_table.apply(self.get_neighbors, axis=1)
        logging.info(f"\n{result}")
        result.to_csv('output.txt', header=[f'# and IDs of Neighbors within {self.r}'], index_label='ID')
    
    def find_candidates(self, center):
        """Map buckets to their contents."""
        all_buckets = np.array(center) + self.hypercube
        all_buckets = [tuple(bucket) for bucket in all_buckets]
        cand_tbl = self.hash_table[self.hash_table['buckets'].isin(all_buckets)]
        return cand_tbl.drop(['buckets'], axis=1)

    def get_neighbors(self, row):
        """For a given node, look up the candidates, and check their distance.
        
        return [n, id1, ..., idn]
        """
        cands = self.candidates[row['buckets']].copy().drop(row.name, axis=0)
        cands['dist'] = np.sqrt(np.sum([(cands[i] - row[i])**2 for i in ('x', 'y', 'z')], axis=0))
        final_cands = cands[cands['dist'] <= self.r]
        result = [len(final_cands)] + list(final_cands.index)
        return result
