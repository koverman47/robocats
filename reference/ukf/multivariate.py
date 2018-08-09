#!/usr/bin/env python

from random import gauss
from ukf import UKF
import numpy.matlib
import numpy as np
import math


R = np.matlib.identity(2, dtype = float) * 0.01
Q = np.matlib.identity(2, dtype = float) * 0.01

def G(data, control):
    for i in range(len(control)):
        for j in range(len(data)):
            data[j][i] = data[j][i] + control[i]
    return data


def H(data, coef=None):
    return data


if __name__ == "__main__":

    delta_t 	    = 1.
    position 	    = np.array([0., 0.])
    velocity 	    = np.array([0., 0.])
    acceleration    = np.array([1., 0.]) # randomly set ~N(0, 1)
    variance        = np.matlib.identity(2, dtype=float) * 0.01
    measurement     = np.array([0., 0.]) # randomly set ~N(position, 1)
    true_position   = np.array([0., 0.])

    ukf = UKF(R, Q, G, H)

   
    for i in range(1, 11):
        acceleration = np.array([gauss(1, 0.1), gauss(1, 0.1)])
        #final_velocity = np.array([velocity[j] + (delta_t * acceleration[j]) for j in range(len(position))])
        final_velocity = np.array([velocity[j] + (delta_t * acceleration[j]) for j in range(len(position))])
        true_position = np.array([true_position[l] + delta_t * ((final_velocity[l] + velocity[l]) / 2) for l in range(len(position))])
        measurement = np.array([gauss(true_position[k], 0.1) for k in range(len(position))])

        position, variance = ukf.get_belief(position, variance, measurement, (final_velocity + velocity) / 2)
        error = true_position - position
        m_error = true_position - measurement
        velocity = np.copy(final_velocity)
        
        print("Time: %s" % i)
        print("Acceleration: %s" % acceleration)
        print("Velocity: %s" % velocity)
        print("True Position: %s" % true_position)
        print("Position: %s" % position)
        print("Estimate Error: %s" % error)
        print("Measurement Error: %s" % m_error)
        print("Measurement: %s" % measurement)
        print("Variance: %s\n\n" % variance)

