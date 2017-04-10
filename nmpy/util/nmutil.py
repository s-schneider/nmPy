from __future__ import absolute_import, print_function
from sipy.util.base import cut2shortest, split2stations


def rotate_stream(stream, rotation='NE->RT'):

	stationlist = split2stations(stream)

	for station in stationlist:
		station = cut2shortest(station)
		station.rotate(rotation)

	return stationlist