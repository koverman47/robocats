#!/usr/bin/env python

import numpy.matlib
import numpy as np


A = np.matlib.identity(2, float)
B = np.array([2, 2])

print(A)
print(B)

#print(np.dot(np.asarray(A), B))
print(np.dot(A, B))
