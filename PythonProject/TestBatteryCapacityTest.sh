#!/bin/sh

tn="BatteryCapacity"

for i in 1 2 5 10; do
	python dispatchGT.py  -pg -ds ../FormattedDataSets/dataElectricGridTariff.csv -tn "$tn" -btrc "$i"
done
