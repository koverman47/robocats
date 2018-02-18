#!/usr/bin/env python3

import time, matrix, numpy as np
from scipy import integrate


class Controller():

    def __init__(self, recursion_depth = 1, kp = 1.0, ki = 0.1, kd = 0.6):
        self.errors = []
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.threshold = 0.001 # Error Threshold: If error < threshold then let error = 0
        self.max_recursion = recursion_depth
        self.transform =    [[1, 1, 0, 0, 0, 0, 0, 0],
                             [0, 0, 1, 1, 0, 0, 0, 0],
                             [0, 0, 0, 0, 1, 1, 1, 1],
                             [0, 0, 0, 0, 0.5, -0.5, 0.5, -0.5],
                             [0, 0, 0, 0, -0.5, -0.5, 0.5, 0.5],
                             [-0.5, 0.5, 0.5, -0.5, 0, 0, 0, 0]] # 6x8 transform: columns represent thrusters, rows: x, y, z, roll, pitch, yaw
        self.inverse = np.linalg.pinv(self.transform).tolist()
        self.clean_inverse() # numpy moore-penrose is bugged
        for r in self.inverse:
            print(r)


    def clean_inverse(self):
        for r in range(len(self.inverse)):
            for c in range(len(self.inverse[r])):
                self.inverse[r][c] = round(self.inverse[r][c], 15)


    # replace errors below threshold with zero
    def test_threshold(self, vector):
        tested = []
        for v in vector:
            if abs(v) < self.threshold:
                tested.append(0)
            else:
                tested.append(v)
        return tested


    # Helper for visualizing errors at the command line
    def print_mean_errors(self):
        mean = 0
        for i in range(len(self.errors[-1])):
            mean += self.errors[-1][i]
        print("MEAN ERROR: %s" % (mean / len(self.errors[-1])))
        print("ERROR: %s" % self.errors[-1])

    # Calculate pid and return transformation (desired forces -> motor commands)
    def get_motor_commands(self, estimated, destination):
        self.errors.append(self.test_threshold(matrix.subtract_vector(destination, estimated)))
        #print("Errors: %s" % self.errors)
        self.print_mean_errors()

        ei = self.get_integral()
        ed = self.get_derivative()
    
        desired = self.pid(self.errors[-1], ei, ed)
        print("\nDesired Forces: %s\n" % desired)
        print("\n##########################################################################################################################################################\n\n")

        return self.calc_motor_commands(desired)

    
    # Transforms 6D forces vector into 8D Motor Commands vector
    def calc_motor_commands(self, desired):
        commands = []

        for r in range(len(self.inverse)):
            sigma = 0
            for c in range(len(self.inverse[r])):
                sigma += desired[c] * self.inverse[r][c] # Apply the transformation on the desired forces vector
            commands.append(sigma)

        large = abs(max(commands, key=abs)) # Get max magnitude for scaling
        for c in range(len(commands)):
            if large != 0:
                commands[c] = commands[c] / large # Scale down to [-1, 1]
            else:
                commands[c] = 0 # Don't divide by zero

        return commands


    
    def get_derivative(self):
        derivative = matrix.recursive_vector_sum(self.errors, min(self.max_recursion, len(self.errors)))
        time = 1.0 / self.max_recursion
        
        for d in range(len(derivative)):
            if self.errors[-1][d] == 0:
                derivative[d] = 0

        return matrix.constant_multiply_vector(derivative, time)


    def get_integral(self):
        if len(self.errors) < self.max_recursion:
            return [0 for k in range(6)]
        data = [0 for m in range(self.max_recursion)]
        integral = []
        for i in range(len(self.errors[-1])):
            for j in range(self.max_recursion):
                data[j] = self.errors[-j][i]
            integral.append(integrate.trapz(data))

        for i in range(len(integral)):
            if self.errors[-1][i] == 4:
                integral[i] = 0
        
        return integral


    def pid(self, ep, ei, ed):
        p = matrix.constant_multiply_vector(ep, self.kp)
        i = matrix.constant_multiply_vector(ei, self.ki)
        d = matrix.constant_multiply_vector(ed, self.kd)
        print("\n\nPID", p, i, d)
        return matrix.add_vector(p, matrix.add_vector(i, d))











