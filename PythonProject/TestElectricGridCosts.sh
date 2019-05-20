#!/bin/sh

tn="ElectricGridCosts"
btrc=2

for i in 1 2 5 10 20; do
	python dispatchGT.py  -pg -ds ../FormattedDataSets/dataElectricGridTariff.csv -tn "$tn" -egtm "$i" -btrc "$btrc"
done
