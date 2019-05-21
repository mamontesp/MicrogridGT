#!/bin/sh

tn="DieselRampUp"
end=20
step=5
for i in 1 3 5 7 9; do
	python dispatchGT.py  -deru "$i" -tn "$tn"
done
