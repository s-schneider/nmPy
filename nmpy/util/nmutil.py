from __future__ import absolute_import, print_function
from sipy.util.base import cut2shortest


def rotate_streamlist(streamlist, rotation='NE->RT'):

	for station in streamlist:
		station = cut2shortest(station)
		station.rotate(rotation)

	return streamlist