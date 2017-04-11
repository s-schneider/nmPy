from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from future.builtins import *  # NOQA @UnusedWildImport

import xdrlib

import numpy as np

from obspy import Stream, Trace, UTCDateTime
from obspy.core.util.attribdict import AttribDict

def _write_ah(stream):
    """
    Reads an AH v1 waveform file and returns a Stream object.

    :type filename: str
    :param filename: AH v1 file to be read.
    :rtype: :class:`~obspy.core.stream.Stream`
    :returns: Stream with Traces specified by given file.
    """

    def _pack_trace(stream):
        ah_stats = AttribDict({
            'version': '1.0',
            'event': AttribDict(),
            'station': AttribDict(),
            'record': AttribDict(),
            'extras': []
        })

        # station info
        packer.pack_string(tr.stats.ah.station.code)
        packer.pack_string(tr.stats.ah.station.channel)
        packer.pack_string(tr.stats.ah.station.type)
        packer.pack_float(tr.stats.ah.station.latitude)
        packer.pack_float(tr.stats.ah.station.longitude)
        packer.pack_float(tr.stats.ah.station.elevation)
        packer.pack_float(tr.stats.ah.station.gain)
        packer.pack_float(tr.stats.ah.station.normalization)

        #Poles and Zeros
        packer.pack_float(len(tr.stats.ah.station.poles))
        packer.pack_float(0)
        packer.pack_float(len(tr.stats.ah.station.zeros))
        packer.pack_float(0)

        poles = tr.stats.ah.station.poles
        zeros = tr.stats.ah.station.zeros
        for _i in range(1,30):
            try:
                r, i = poles[_i].real, poles[_i].imag
            except IndexError:
                r, i = 0, 0
            packer.pack_float(r)
            packer.pack_float(i)

            try:
                r, i = zeros[_i].real, zeros[_i].imag
            except IndexError:
                r, i = 0, 0
            packer.pack_float(r)
            packer.pack_float(i)           

        # event info

        packer.pack_float(tr.stats.ah.event.latitude)
        packer.pack_float(tr.stats.ah.event.longitude)
        packer.pack_float(tr.stats.ah.event.depth)



        # ah_stats.event.latitude = data.unpack_float()
        # ah_stats.event.longitude = data.unpack_float()
        # ah_stats.event.depth = data.unpack_float()
        # ot_year = data.unpack_int()
        # ot_mon = data.unpack_int()
        # ot_day = data.unpack_int()
        # ot_hour = data.unpack_int()
        # ot_min = data.unpack_int()
        # ot_sec = data.unpack_float()
        # try:
        #     ot = UTCDateTime(ot_year, ot_mon, ot_day, ot_hour, ot_min, ot_sec)
        # except:
        #     ot = None
        # ah_stats.event.origin_time = ot
        # ah_stats.event.comment = _unpack_string(data)

        # # record info
        # ah_stats.record.type = dtype = data.unpack_int()  # data type
        # ah_stats.record.ndata = ndata = data.unpack_uint()  # number of samples
        # ah_stats.record.delta = data.unpack_float()  # sampling interval
        # ah_stats.record.max_amplitude = data.unpack_float()
        # at_year = data.unpack_int()
        # at_mon = data.unpack_int()
        # at_day = data.unpack_int()
        # at_hour = data.unpack_int()
        # at_min = data.unpack_int()
        # at_sec = data.unpack_float()
        # at = UTCDateTime(at_year, at_mon, at_day, at_hour, at_min, at_sec)
        # ah_stats.record.start_time = at
        # ah_stats.record.abscissa_min = data.unpack_float()
        # ah_stats.record.comment = _unpack_string(data)
        # ah_stats.record.log = _unpack_string(data)

        # # extras
        # ah_stats.extras = data.unpack_array(data.unpack_float)

        # # unpack data using dtype from record info
        # if dtype == 1:
        #     # float
        #     temp = data.unpack_farray(ndata, data.unpack_float)
        # elif dtype == 6:
        #     # double
        #     temp = data.unpack_farray(ndata, data.unpack_double)
        # else:
        #     # e.g. 3 (vector), 2 (complex), 4 (tensor)
        #     msg = 'Unsupported AH v1 record type %d'
        #     raise NotImplementedError(msg % (dtype))
        # tr = Trace(np.array(temp))
        # tr.stats.ah = ah_stats
        # tr.stats.delta = ah_stats.record.delta
        # tr.stats.starttime = ah_stats.record.start_time
        # tr.stats.station = ah_stats.station.code
        # tr.stats.channel = ah_stats.station.channel

    packer = xdrlib.Packer()

    for tr in stream:
        if tr.stats._format in ('AH'):
            ahform = True
        else:
            ahform = False

    if ahform:
        for tr in stream:
            _pack_trace(tr, packer)

