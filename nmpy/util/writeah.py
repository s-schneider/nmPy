from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from future.builtins import *  # NOQA @UnusedWildImport

import xdrlib

import numpy as np

from obspy import Stream, Trace, UTCDateTime
from obspy.core.util.attribdict import AttribDict

def _write_ah(stream, filename):
    """
    Reads an AH v1 waveform file and returns a Stream object.

    :type filename: str
    :param filename: AH v1 file to be read.
    :rtype: :class:`~obspy.core.stream.Stream`
    :returns: Stream with Traces specified by given file.
    """

    def _pack_trace(trace, packer):


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
        packer.pack_int(tr.stats.ah.event.origin_time.year)
        packer.pack_int(tr.stats.ah.event.origin_time.month)
        packer.pack_int(tr.stats.ah.event.origin_time.day)
        packer.pack_int(tr.stats.ah.event.origin_time.hour)
        packer.pack_int(tr.stats.ah.event.origin_time.minute)
        packer.pack_float(tr.stats.ah.event.origin_time.second)
        packer.pack_string(tr.stats.ah.event.comment)

        # record info
        dtype = tr.stats.ah.record.type
        packer.pack_int(dtype)
        ndata = tr.stats.ah.record.ndata
        packer.pack_uint(ndata)
        packer.pack_float(tr.stats.ah.record.delta)
        packer.pack_float(tr.stats.ah.record.max_amplitude)
        packer.pack_int(tr.stats.ah.record.start_time.year)
        packer.pack_int(tr.stats.ah.record.start_time.month)
        packer.pack_int(tr.stats.ah.record.start_time.day)
        packer.pack_int(tr.stats.ah.record.start_time.hour)
        packer.pack_int(tr.stats.ah.record.start_time.minute)
        packer.pack_float(tr.stats.ah.record.start_time.second)
        packer.pack_float(tr.stats.ah.record.abscissa_min)
        packer.pack_string(tr.stats.ah.record.comment)
        packer.pack_string(tr.stats.ah.record.log)

        # # extras
        packer.pack_array(tr.stats.ah.extras, packer.pack_float)

        # pack data using dtype from record info
        if dtype == 1:
            # float
            packer.pack_farray(ndata, tr.data, packer.pack_float)
        elif dtype == 6:
            # double
            packer.pack_farray(ndata, tr.data, packer.pack_double)
        else:
            # e.g. 3 (vector), 2 (complex), 4 (tensor)
            msg = 'Unsupported AH v1 record type %d'
            raise NotImplementedError(msg % (dtype))

        return packer



    for tr in stream:
        if tr.stats._format in ('AH'):
            ahform = True
        else:
            ahform = False

    if ahform:
        
        for i, tr in enumerate(stream):
            ofilename = filename + str(i) + ".AH"

            packer = xdrlib.Packer()
            #write Version number: here V1
            magic = 6
            packer.pack_int(magic)
            with open(ofilename, 'wb') as fh:
                fh.write(packer.get_buffer())

            #reinitialize packer
            packer = None
            packer = xdrlib.Packer()

            packer = _pack_trace(tr, packer)

            with open(ofilename, 'ab') as fh:
                fh.write(packer.get_buffer())

            #reset packer
            packer = None

    else:

        print("Input Stream not in AH format")



