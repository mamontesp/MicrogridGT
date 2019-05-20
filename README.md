# MicrogridGT

MicrogridGT is a Python library for dealing with dispatch of energy resources in a constrained environment

## Usage
To run created tests
```sh
sh ./TestDieselRampUp.sh
sh ./TestElectricGridCosts.sh 
```
To test directly in python
```python
dispatchGT.py [-h] [-a ALPHA] [-d1 POWERBALANCE] [-d2 NASHEQUILIBRIUM]
                     [-pvuep PVUEP] [-wtuep WTUEP] [-deuep DEUEP]
                     [-btuep BTUEP] [-lduep LDUEP] [-egtm EGTM] [-pvumc PVUMC]
                     [-wtumc WTUMC] [-deumc DEUMC] [-btumc BTUMC]
                     [-egumc EGUMC] [-deop DEOILPRICE]
                     [-derc DERATECONSUMPTION] [-demin DEMINPOWER]
                     [-demax DEMAXPOWER] [-deru DERAMPUP] [-derd DERAMPDOWN]
                     [-demrt DEMINRUNNINGTIME] [-deaoc DEAOILCONSUMPTION]
                     [-deboc DEBOILCONSUMPTION] [-decoc DECOILCONSUMPTION]
                     [-btsd BTSELFDIS] [-btrc BTRATEDCAP] [-btc BTC]
                     [-btde BTDISCHARGEEFF] [-btce BTCHARGEEFF]
                     [-btsmx BTSOCMAX] [-btsmn BTSOCMIN] [-btsi BTSOCINIT]
                     [-ldws LDWEIGHTSAT] [-ldb LDBETA] [-lda LDALPHA]
                     [-tn TESTNAME] [-sa SAMPLESTOANALIZE] [-pg] [-ds DATASET]

```

name of variable | (Default value)| Description
-----------------|----------------|------------
alpha  |(ALPHA): |  Weight of power balance
powerbalance |(POWERBALANCE): |  Update of alpha in case power balance is not reached
nashequilibrium NASHEQUILIBRIUM : |  Update of alpha in case nash equilibrium is not reached
pvuep  |(PVUEP): |  Photovoltaics unit electric price
wtuep  |(WTUEP): |  Wind turbine unit electric price
deuep  |(DEUEP): |  Diesel unit electric price
btuep  |(BTUEP): |  Battery unit electric price
lduep  |(LDUEP): |  Load unit electric price
egtm |(EGTM): |  Electric grid unit tariff multiplier
pvumc  |(PVUMC): |  Photovoltaics unit maintenance cost
wtumc  |(WTUMC): |  Wind turbine unit maintenance cost
deumc  |(DEUMC): |  Diesel unit maintenance cost
btumc  |(BTUMC): |  Battery unit maintenance cost
egumc  |(EGUMC): |  Electric grid unit maintenance cost
deoilprice |(DEOILPRICE): |  Oil price. Be consistent with units of DE_RC
derateconsumption  |(DERATECONSUMPTION): |  Oil rate consumption. Be consistent with units of DE_OP
deminpower |(DEMINPOWER): |  Min diesel power
demaxpower |(DEMAXPOWER): |  Max diesel power
derampup |(DERAMPUP): |  Diesel ramp up diesel
derampdown |(DERAMPDOWN): |  Diesel ramp down diesel
deminrunningtime |(DEMINRUNNINGTIME): |  Diesel min running time
deaoilconsumption  |(DEAOILCONSUMPTION): |  Factor to model quadratic term in diesel consumtion function
deboilconsumption  |(DEBOILCONSUMPTION): |  Factor to model linear term in diesel consumtion function
decoilconsumption  |(DECOILCONSUMPTION): |  Factor to model constant term in diesel consumtion function
btselfdis  |(BTSELFDIS): |  Battery self discharge by operating cycle
btratedcap |(BTRATEDCAP): |  Battery rated capacity in kWh
btc  |(BTC): |  C factor to model battery behavior
btdischargeeff |(BTDISCHARGEEFF): |  Discharge efficiency in battery
btchargeeff  |(BTCHARGEEFF): |  Charge efficiency in battery
btsocmax |(BTSOCMAX): |  Max SOC allowed in battery in percentage. Usually 100
btsocmin |(BTSOCMIN): |  Min SOC allowed in battery in percentage.
btsocinit  |(BTSOCINIT): |  Starting SOC for simulation.
ldweightsat  |(LDWEIGHTSAT): |  Load weight factor of satisfaction.
ldbeta |(LDBETA): |  Factor to model satisfaction of load function
ldalpha  |(LDALPHA): |  Factor to model satisfaction of load function
testname |(TESTNAME): |  Folder name to save tests to run
samplestoanalize |(SAMPLESTOANALIZE): |  Number of units of time to analize
playwithgrid |(TRUE): | Play with electric grid
dataset  |(DATASET): |  Name of dataset for initial resources and load data
-----------------|----------------|------------

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
