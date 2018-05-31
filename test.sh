#!/bin/bash

ID_LEN=6
for i in $(ls images); do
    echo "Image: $i"
    expected=$(echo $i | head -c $ID_LEN | tail -c 1)
    out=$(./guess.py "images/$i") 
    echo "$out"
    found=$(echo "$out" | tail -n 1)
    echo "Expected:  $expected"
    echo "Found: $found"
    echo
done

