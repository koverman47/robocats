#!/bin/bash

g++ $1 -o a.out
./a.out
rm -f a.out
