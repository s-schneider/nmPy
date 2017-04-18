from __future__ import absolute_import, print_function
from sipy.util.base import cut2shortest, split2stations


def rotate_stream(stream, rotation='NE->RT', merge=True):
	"""
	Sorts stream by stations and rotates them. If keep_all_components is False, only stations with records of Z, E, N component will be kept
	"""
	stl = split2stations(stream, merge)


	for station in stl:
		try:
			station.rotate(rotation)
		except ValueError:
			cut2shortest(station)
			station.rotate(rotation)

		station.sort(['channel'])

	return stl