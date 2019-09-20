#!/bin/sh

tn="battery_capacity"

for i in 1 2 5 10; do
	python main.py  -pg -ds formatted_datasets/dataElectricGridTariff.csv -tn "$tn" -btrc "$i"
done
