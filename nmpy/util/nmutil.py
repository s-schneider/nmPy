from __future__ import absolute_import, print_function
from sipy.util.base import cut2shortest, split2stations


def rotate_stream(stream, rotation='NE->RT', only_3_components=True, merge=True):
	"""
	Sorts stream by stations and rotates them. If keep_all_components is False, only stations with records of Z, E, N component will be kept
	"""
	stationlist = split2stations(stream, merge)

	for i, station in enumerate(stationlist):
		if only_3_components:
			if len(station) != 3:
				stationlist.pop(i)
				continue
		station = cut2shortest(station)
		station.rotate(rotation)

	return stationlist