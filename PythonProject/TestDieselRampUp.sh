#!/bin/sh

tn="DieselRampUp"
end=20
step=5
for i in 5 10 15 20; do
	python dispatchGT.py  -deru "$i" -tn "$tn"
done
