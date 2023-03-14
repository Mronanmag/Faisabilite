from Bio import Phylo
import sys
import matplotlib
import pylab

input_path = sys.argv[1]
output_path = sys.argv[2]

tree=Phylo.read(input_path,'newick')
Phylo.draw_ascii(tree)

