from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from future.builtins import *  # NOQA @UnusedWildImport

import xdrlib

import numpy as np

from obspy import Stream, Trace, UTCDateTime
from obspy.core.util.attribdict import AttribDict

def _write_ah1(stream, filename, channelfiles=False):
    """
    Reads an AH v1 waveform file and returns a Stream object.

    :type filename: str
    :param filename: AH v1 file to be read.
    :rtype: :class:`~obspy.core.stream.Stream`
    :returns: Stream with Traces specified by given file.
    """

    CODESIZE  = 6
    CHANSIZE  = 6
    STYPESIZE = 8
    COMSIZE   = 80
    TYPEMIN   = 1
    TYPEMAX   = 6
    LOGSIZE   = 202
    LOGENT    = 10
    NEXTRAS   = 21
    NOCALPTS  = 30

    def _pack_trace_with_ah_dict(trace, packer):

        # station info
        packer.pack_int(CODESIZE)
        packer.pack_fstring(CODESIZE, tr.stats.ah.station.code)
        packer.pack_int(CHANSIZE)
        try:
            packer.pack_fstring(CHANSIZE, tr.stats.channel)
        except:
            packer.pack_fstring(CHANSIZE, tr.stats.ah.station.channel)

        packer.pack_int(STYPESIZE)
        packer.pack_fstring(STYPESIZE,tr.stats.ah.station.type)
        packer.pack_float(tr.stats.ah.station.latitude)
        packer.pack_float(tr.stats.ah.station.longitude)
        packer.pack_float(tr.stats.ah.station.elevation)
        packer.pack_float(tr.stats.ah.station.gain)
        packer.pack_float(tr.stats.ah.station.normalization)

        poles = tr.stats.ah.station.poles
        zeros = tr.stats.ah.station.zeros

        #Poles and Zeros
        packer.pack_float(len(poles))
        packer.pack_float(0)
        packer.pack_float(len(zeros))
        packer.pack_float(0)

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
        try:
            packer.pack_int(tr.stats.ah.event.origin_time.year)
            packer.pack_int(tr.stats.ah.event.origin_time.month)
            packer.pack_int(tr.stats.ah.event.origin_time.day)
            packer.pack_int(tr.stats.ah.event.origin_time.hour)
            packer.pack_int(tr.stats.ah.event.origin_time.minute)
            packer.pack_float(tr.stats.ah.event.origin_time.second)
        except:
            packer.pack_int(0)
            packer.pack_int(0)
            packer.pack_int(0)
            packer.pack_int(0)
            packer.pack_int(0)
            packer.pack_float(0)

        packer.pack_int(COMSIZE)
        packer.pack_fstring(COMSIZE, tr.stats.ah.event.comment)

        # record info
        dtype = tr.stats.ah.record.type
        packer.pack_int(dtype)
        ndata = tr.stats.npts
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
        packer.pack_int(COMSIZE)
        packer.pack_fstring(COMSIZE, tr.stats.ah.record.comment)
        packer.pack_int(LOGSIZE)
        packer.pack_fstring(LOGSIZE,tr.stats.ah.record.log)

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

    def _pack_trace_wout_ah_dict(trace, packer):
        # Entry are packed in the same order as shown in _pack_trace_with_ah_dict
        # The missing information is replaced with zeros
        # station info
        packer.pack_int(CODESIZE)
        packer.pack_fstring(CODESIZE, tr.stats.station)
        packer.pack_int(CHANSIZE)
        packer.pack_fstring(CHANSIZE, tr.stats.channel)
        packer.pack_int(STYPESIZE)
        packer.pack_fstring(STYPESIZE,'null')
        # There is no information about latitude, longitude, elevation, 
        # gain and normalization in the basic stream object,  are set to 0
        packer.pack_float(0)
        packer.pack_float(0)
        packer.pack_float(0)
        packer.pack_float(0)
        packer.pack_float(0)

        #Poles and Zeros are not provided by stream object, are set to 0
        for _i in range(0,30):
            packer.pack_float(0)
            packer.pack_float(0)
            packer.pack_float(0)
            packer.pack_float(0)           

        # event info
        packer.pack_float(0)
        packer.pack_float(0)
        packer.pack_float(0)
        packer.pack_int(0)
        packer.pack_int(0)
        packer.pack_int(0)
        packer.pack_int(0)
        packer.pack_int(0)
        packer.pack_float(0)

        packer.pack_int(COMSIZE)
        packer.pack_fstring(COMSIZE, 'null')

        # record info
        dtype = type(tr.data[0])
        if '32' in str(dtype):
            dtype = 1
        elif '64' in str(dtype):
            dtype = 6

        packer.pack_int(dtype)
        ndata = tr.stats.npts
        packer.pack_uint(ndata)
        packer.pack_float(tr.stats.delta)
        packer.pack_float(max(tr.data))
        packer.pack_int(tr.stats.starttime.year)
        packer.pack_int(tr.stats.starttime.month)
        packer.pack_int(tr.stats.starttime.day)
        packer.pack_int(tr.stats.starttime.hour)
        packer.pack_int(tr.stats.starttime.minute)

        starttime_second = float(str(tr.stats.starttime.second) + '.' + str(tr.stats.starttime.microsecond))
        packer.pack_float(starttime_second)

        packer.pack_float(0)
        packer.pack_int(COMSIZE)
        packer.pack_fstring(COMSIZE, 'null')
        packer.pack_int(LOGSIZE)
        packer.pack_fstring(LOGSIZE, 'null')

        # # extras
        packer.pack_array(np.zeros(21).tolist(), packer.pack_float)

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



    packer = xdrlib.Packer()

    for tr in stream:
        if hasattr(tr.stats, 'ah'):
            packer = _pack_trace_with_ah_dict(tr, packer)
        else:
            packer = _pack_trace_wout_ah_dict(tr, packer)

        if channelfiles:
            ofilename = filename + "." + tr.stats.channel + ".AH"
            with open(ofilename, 'wb') as fh:
                fh.write(packer.get_buffer())
            packer.reset()

    if not channelfiles:
        ofilename = filename + ".AH"
        with open(ofilename, 'wb') as fh:
            fh.write(packer.get_buffer())
