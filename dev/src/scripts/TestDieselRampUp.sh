#!/bin/sh

tn="diesel_ramp_up"
end=20
step=5
for i in 1 3 5 7 9; do
	python main.py  -deru "$i" -tn "$tn"
done
