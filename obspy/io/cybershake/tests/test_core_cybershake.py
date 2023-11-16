# -*- coding: utf-8 -*-
"""
The cybershake.core test suite.
"""
import numpy as np
from obspy import read
from obspy.io.cybershake.core import _is_cybershake, _read_cybershake


class TestCybershake():
    """
    Testing reading of CyberShake seismograms.
    """
    def test_read_cybershake(self, testdata):
        valid_file = testdata['test.grm']
        invalid_file = testdata['not_cybershake.grm']
        # Check that two files are/are not valid CyberShake data
        assert _is_cybershake(valid_file)
        assert not _is_cybershake(invalid_file)

        # Test reading the data using both _read_cybershake and read
        st1 = _read_cybershake(valid_file)
        st2 = read(valid_file)
        for st in [st1, st2]:
            assert len(st) == 2
            for tr in st:
                assert tr.stats.network == 'CS'
                assert tr.stats.station == 'USC'
                assert tr.stats.location == '00'
                assert len(tr.data) == 8000
                assert np.allclose(tr.stats.delta, 0.05)
                assert tr.stats.cybershake.source_id == 12
                assert tr.stats.cybershake.rupture_id == 0
                assert tr.stats.cybershake.rup_var_id == 144
            assert st[0].stats.channel == 'MXE'
            assert st[1].stats.channel == 'MXN'
            assert np.allclose(st[0].data[1000], -0.6695289015769958)
            assert np.allclose(st[1].data[1000], 0.04939334839582443)
