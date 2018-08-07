#!/usr/bin/env python

from random import gauss
from ukf import UKF
import numpy.matlib
import numpy as np
import math


R = np.matlib.identity(2, dtype = float) * 0.01
Q = np.matlib.identity(2, dtype = float) * 0.01

def G():
    pass


def H():
    pass


if __name__ == "__main__":

    delta_t 	    = 1.
    position 	    = np.matlib.zeros((2, 2))
    velocity 	    = np.matlib.zeros((2, 2))
    acceleration    = np.matlib.zeros((2, 2)) # randomly set ~N(0, 1)
    variance        = np.matlib.identity(4, dtype=float) * 0.1
    measurement     = np.matlib.zeros((2, 2)) # randomly set ~N(position, 1)

    true_position   = np.matlib.zeros((2, 2))

    ukf = UKF(R, Q, G, H)

   
    for i in range(1, 11):
        #acceleration = gauss(0, 1)
        acceleration = np.array([1, 0])
        final_velocity = np.array([velocity + (delta_t * acceleration[i]) for i in range(len(position))])
        true_position = np.array([delta_t * ((final_velocity[i] + velocity[i]) / 2) for i in range(len(position))])
        measurement = np.array([gauss(true_position, 0.1) for i in range(len(position))])
        velocity = np.copy(final_velocity)

        position, variance = ukf.get_belief(position, variance, measurement, velocity)
        error = true_position - position
        
        print("Time: %s" % i)
        print("Position: %s" % position)
        print("True Position: %s" % true_position)
        print("Error: %s\n" % error)
        print("Velocity: %s" % velocity)
        print("Acceleration: %s" % acceleration)
        print("Measurement: %s" % measurement)
        print("Variance: %s\n\n" % variance)

