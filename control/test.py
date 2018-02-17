#!/usr/bin/env python3

import time, matrix, random
from controller import Controller


DELAY = 1
ITERATIONS = 10000
transform = None


# (current state, desired_state, commands)
def init_system():
    return ([0, 0, 0, 0, 0, 0], [0, 0, 2, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0])


def get_next_state(state, commands):
    next_state = []
    for r in range(len(transform)):
        sigma = 0
        for c in range(len(commands)):
            sigma += transform[r][c] * commands[c]
        next_state.append((sigma * 0.001 * DELAY) + state[r])
        #next_state.append((sigma * 0.1 * DELAY) + random.gauss(0, 0.05) + state[r])
        pass
    
    return next_state


def print_status(state, commands, desired, counter):
    print("\n##########################################################################################################################################################")
    print("STATUS NUMBER: %s" % counter)
    print("Desired: %s\n" % desired)
    print("State: %s\n" % state)
    print("Commands: %s\n" % commands)


if __name__ == "__main__":
    
    controller = Controller(3, 0.8, 0, .75)
    transform = controller.transform

    current_state, desired_state, commands = init_system()

    counter = 1
    while 1:
        print_status(current_state, commands, desired_state, counter)
        if counter > ITERATIONS:
            break
        counter += 1

        commands = controller.get_motor_commands(current_state, desired_state)
    
        current_state = get_next_state(current_state, commands)

        #time.sleep(DELAY)

