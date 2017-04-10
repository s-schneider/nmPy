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

def safe_streamlist(streamlist, format='AH'):

	for station in streamlist:
		time  = station[0].stats.starttime
		name    = station[0].stats.station
		network = station[0].stats.network
		try:
			location = station[0].stats.location
		except:
			location = ''
		try:
			quality =  station[0].stats.mseed['dataquality']
		except:
			quality =  ''

		fname = str(time.format_seed()).replace(",",".") + "." + network + "." + name + "." + location + "." + quality + "." + format

		try:
			station.write(fname, format=format)
		except:
			continue
