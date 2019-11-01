import sys
import math

IS_PYTHON_2 = sys.version_info < (3,)


def compare_float(f1, f2, precision=0.0000001):
    return math.fabs(f1-f2)<precision


def compare_complex(c1, c2, precision=0.0000001):
    return compare_float(c1.real, c2.real, precision) and\
           compare_float(c1.imag, c2.imag, precision)
