"""
Author: Maksim Korolev
Folder Traversing & Matching Function
"""

import os
import sys
import re
from matplotlib import pyplot as pl
import numpy as np

#use global lists so recursive function can append
matches, Xs, Ys = [], [], []

#recursive function to count files that match RE/keyword in each directory
#count and directory path appended to matches in the form path:count
def find_files(root_dir, keyword):
	count = 0
	for item in os.listdir(root_dir):
		path = os.path.join(root_dir, item)
		if os.path.isfile(path):
			if re.search(keyword, item) != None:
				count += 1
		else:
			find_files(path, keyword)
	matches.append(root_dir + ":" + str(count))
	Xs.append(root_dir)
	Ys.append(count)

#creates a bar graph sorted with subdirectories with most matched filenames on right
def create_plot(Xs, Ys, keyword):
	fig = pl.figure()
	width = .75
	ind = np.arange(len(Xs))
	pl.bar(ind, Ys)
	pl.ylabel('Number of Matches')
	pl.title("Number of Files in Each Subdirectory that Match: " + keyword)
	pl.xlabel("Subdirectory")
	pl.xticks(ind + width/2 , Xs)
	fig.autofmt_xdate()
	pl.show()

def function(root_dir, keyword):
	global matches, Xs, Ys
	matches, Xs, Ys = [], [], []
	find_files(root_dir, keyword)
	sortedYs, sortedXs = (list(t) for t in zip(*sorted(zip(Ys, Xs))))
	create_plot(sortedXs, sortedYs, keyword)
	return sorted(matches)

if __name__ == '__main__':
	if len(sys.argv) > 1:
		function(sys.argv[1], sys.argv[2])