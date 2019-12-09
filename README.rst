========
AtomNeighbors
========
A script for determining nearest-neighbors within a radius.

Install
=======
In the root directory,

    pip install . 

For a development install,

    pip install -r requirements.txt

Usage
=====
On the command line, to load nodes from `input.txt` and specify a search radius of 1.0,

    atomneighbors -p input.txt -r 1.0

Instead of the `-p` flag to specify an input filepath, you may specify a number of
nodes to randomly generate with `-n`. Note that the nodes will be uniformly distributed
in a range from -10^7 to 10^7 in all directions. 

The output will be printed to stdout (unless the `-q` flag is used), and written to
`output.txt` in the current working directory. 

The `-t` flag causes the runtime to be reported. 
