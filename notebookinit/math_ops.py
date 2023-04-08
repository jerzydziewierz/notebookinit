import numpy
from math import tau


def circular_diff(pa, pb, modulo=tau):
    """
    Compute the difference between two eulerian angles in a circular space.
    The result is always in the range [-modulo/2, modulo/2].
    """
    pa = numpy.expand_dims(numpy.array(pa), axis=-1)
    pb = numpy.expand_dims(numpy.array(pb), axis=-1)
    mod_pa = numpy.mod(numpy.array(pa), modulo)
    mod_pb = numpy.mod(numpy.array(pb), modulo)
    possible_diffs = numpy.stack([mod_pa-mod_pb-modulo, mod_pa-mod_pb, mod_pa+mod_pb-modulo])

    best_diff = numpy.argmin(numpy.abs(possible_diffs), axis=0)
    result = numpy.squeeze(numpy.choose(best_diff,possible_diffs))
    return result