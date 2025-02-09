#!/bin/bash
mkdir bin 2>/dev/null
g++ -std=c++11 -O3 -o bin/2.out src/2.cpp -lm
