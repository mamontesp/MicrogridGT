#!/bin/sh

tn="electric_grid_costs"
btrc=2

for i in 1 2 5 10 20; do
	python main.py  -pg -ds  formatted_datasets/dataElectricGridTariff.csv -tn "$tn" -egtm "$i" -btrc "$btrc"
done
