#!/bin/bash
mkdir bin 2>/dev/null
g++ -std=c++11 -O3 -o bin/1.out src/1.cpp -lm
