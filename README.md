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

Name of variable | Default value| Description
-----------------|----------------|------------
alpha  |ALPHA = 0.1 |  Weight of power balance
powerbalance |POWERBALANCE = 2|  Update of alpha in case power balance is not reached
nashequilibrium | NASHEQUILIBRIUM = 4 |  Update of alpha in case nash equilibrium is not reached
pvuep  |PV_UEP =  2  |  Photovoltaics unit electric price
wtuep  |WT_UEP =  4  |  Wind turbine unit electric price
deuep  |DE_UEP =  4  |  Diesel unit electric price
btuep  |BT_UEP =  0.1|  Battery unit electric price
lduep  |LD_UEP =  0.4|  Load unit electric price
egtm |EGTM =  20|  Electric grid unit tariff multiplier
pvumc  |PV_UMC = 0.5 |  Photovoltaics unit maintenance cost
wtumc  |WT_UMC = 3.0 |  Wind turbine unit maintenance cost
deumc  |DE_UMC = 3.0 |  Diesel unit maintenance cost
btumc  |BT_UMC = 0.05|  Battery unit maintenance cost
egumc  |EG_UMC = 0.02|  Electric grid unit maintenance cost
deoilprice |DE_OP = 3.0  |  Oil price. Be consistent with units of DE_RC
derateconsumption  |DE_RC = 2 |  Oil rate consumption. Be consistent with units of DE_OP
deminpower |DE_MIN = 0 |  Min diesel power
demaxpower |DE_MAX = 10 |  Max diesel power
derampup |DE_RAMP_UP = 20 |  Diesel ramp up diesel
derampdown |DE_RAMP_DOWN = 10  |  Diesel ramp down diesel
deminrunningtime |DE_MIN_RUNNING_TIME = 0.3  |  Diesel min running time
deaoilconsumption  |DE_A_OIL_CONSUMPTION = 1 |  Factor to model quadratic term in diesel consumtion function
deboilconsumption  |DE_B_OIL_CONSUMPTION = 2  |  Factor to model linear term in diesel consumtion function
decoilconsumption  |DE_C_OIL_CONSUMPTION = 1  |  Factor to model constant term in diesel consumtion function
btselfdis  |BT_SELF_DIS = 0.0000001 |  Battery self discharge by operating cycle
btratedcap |BT_RATED_CAP = 10  |  Battery rated capacity in kWh
btc  |BTC =  |  C factor to model battery behavior
btdischargeeff |BT_DIS_EFF = 0.99  |  Discharge efficiency in battery
btchargeeff  |BT_CHAR_EFF = 0.99 |  Charge efficiency in battery
btsocmax |BT_SOC_MAX = 100 |  Max SOC allowed in battery in percentage. Usually 100
btsocmin |BT_SOC_MIN = 60  |  Min SOC allowed in battery in percentage.
btsocinit  |BT_SOC_INIT = 70  |  Starting SOC for simulation.
ldweightsat  |LD_WEIGHT_SAT = 0.9 |  Load weight factor of satisfaction.
ldbeta |LD_BETA = -1  |  Factor to model satisfaction of load function
ldalpha  |LD_ALPHA = 0.5  |  Factor to model satisfaction of load function
testname |TEST_NAME = Test  |  Folder name to save tests to run
samplestoanalize |SAMPLES_TO_ANALIZE = 20  |  Number of units of time to analize
playwithgrid |TRUE if -pg included | Option to include player electric grid to the game
dataset  |DATA_SET_FILE_NAME =  '../FormattedDataSets/dataWithoutBatteries.csv' |  Name of dataset for initial resources and load data

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
