#!/bin/sh

tn="plug_and_play_grid"
btrc=2
egtm=5

python main.py  -ds  formatted_datasets/dataElectricGridTariff.csv -tn "$tn" -btrc "$btrc"
python main.py  -pg -ds  formatted_datasets/dataElectricGridTariff.csv -tn "$tn" -egtm "$egtm" -btrc "$btrc"

