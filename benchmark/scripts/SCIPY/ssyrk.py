#!/usr/bin/env python

import os
import sys
import time
import numpy
from numpy import zeros
from numpy.random import randn
from scipy.linalg import blas


def run_ssyrk(N, l):

    A = randn(N, N).astype('float32', order='F')
    C = zeros((N, N), dtype='float32', order='F')

    start = time.time()
    for _ in range(0, l):
        blas.ssyrk(1.0, A, c=C, overwrite_c=True)
    end = time.time()

    timediff = (end - start)
    mflops = (N * N * N) * l / timediff
    mflops *= 1e-6

    size = "%dx%d" % (N, N)
    print("%14s :\t%20f MFlops\t%20f sec" % (size, mflops, timediff))


if __name__ == "__main__":
    N = 128
    NMAX = 2048
    NINC = 128
    LOOPS = 1

    z = 0
    for arg in sys.argv:
        if z == 1:
            N = int(arg)
        elif z == 2:
            NMAX = int(arg)
        elif z == 3:
            NINC = int(arg)
        elif z == 4:
            LOOPS = int(arg)

        z = z + 1

    if 'OPENBLAS_LOOPS' in os.environ:
        if p := os.environ['OPENBLAS_LOOPS']:
            LOOPS = int(p)

    print("From: %d To: %d Step=%d Loops=%d" % (N, NMAX, NINC, LOOPS))
    print("\tSIZE\t\t\tFlops\t\t\t\t\tTime")

    for i in range(N, NMAX + NINC, NINC):
        run_ssyrk(i, LOOPS)
