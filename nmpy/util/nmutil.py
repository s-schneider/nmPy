from __future__ import absolute_import, print_function
from sipy.util.base import cut2shortest, split2stations, list2stream


def rotate_stream(stream, rotation='NE->RT', merge=False, format='stream'):
	"""
	Sorts stream by stations and rotates them. Returns a list of streams or a stream
	"""
	stl = split2stations(stream, merge)

	for station in stl:
		try:
			station.rotate(rotation)
		except ValueError:
			cut2shortest(station)
			station.rotate(rotation)

		station.sort(['channel'])


	if format ==  'stream':
		st = list2stream(stl)
	else:
		st = stl

	return st

