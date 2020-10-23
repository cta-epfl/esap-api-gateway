"""
common helper functions
"""
import logging;
from datetime import *
import time

from astropy.coordinates import SkyCoord

logger = logging.getLogger(__name__)

# this is a decorator that can be put in front (around) a function all to measure its execution time
def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print('execution time: %r  %2.2f ms' % \
                  (method.__name__, (te - ts) * 1000))
        return result
    return timed


def get_sky_coords(target_name):
    # convert object name to sky coordinates
    # target_coords = SkyCoord.from_name(target_name)
    # Resolved coordinates is
    # <SkyCoord (ICRS): (ra, dec) in deg
    # (258.2085, 64.05294444)>
    # target_coords.ra.deg, target_coords.dec.deg
    # target_coords.ra.rad, target_coords.dec.rad

    target_coords = SkyCoord.from_name(target_name)
    return target_coords
