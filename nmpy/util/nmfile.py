from __future__ import absolute_import, print_function
import os

def read_dat_folder(folder):
	tmp_l = os.listdir(folder)
	flist = []

	for file in tmp_l:
		if file.endswith('.dat'):
			file = folder + file
			flist.append(file)
	flist.sort()

	return flist