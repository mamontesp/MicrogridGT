#!/bin/sh

tn="PNPGrid"
btrc=2
egtm=5

python dispatchGT.py  -ds ../FormattedDataSets/dataElectricGridTariff.csv -tn "$tn" -btrc "$btrc"
python dispatchGT.py  -pg -ds ../FormattedDataSets/dataElectricGridTariff.csv -tn "$tn" -egtm "$egtm" -btrc "$btrc"

