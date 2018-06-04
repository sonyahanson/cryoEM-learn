#!/bin/bash

# This script makes a simple list of particles you can use
# to reconstruct volumes with reconst_test.bat in Spider.
# USAGE: ./make_listparticles.sh > listparticles_95k.spi

echo ' ;mat/spi   3-Apr-2018 AT 17:49   listparticles_95k.spi'
for i in {1..95000}
do
    printf '%5d  1      %5d \n' "$i" "$i"
done
