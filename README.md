# MicrogridGT

MicrogridGT is a Python library for dealing with dispatch of energy resources in a constrained environment

## Usage

```sh
sh ./TestDieselRampUp.sh
sh ./TestElectricGridCosts.sh 
```
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

-a ALPHA, --alpha ALPHA
                        Weight of power balance
  -d1 POWERBALANCE, --powerbalance POWERBALANCE
                        Update of alpha in case power balance is not reached
  -d2 NASHEQUILIBRIUM, --nashequilibrium NASHEQUILIBRIUM
                        Update of alpha in case nash equilibrium is not
                        reached
  -pvuep PVUEP, --pvuep PVUEP
                        Photovoltaics unit electric price
  -wtuep WTUEP, --wtuep WTUEP
                        Wind turbine unit electric price
  -deuep DEUEP, --deuep DEUEP
                        Diesel unit electric price
  -btuep BTUEP, --btuep BTUEP
                        Battery unit electric price
  -lduep LDUEP, --lduep LDUEP
                        Load unit electric price
  -egtm EGTM, --egtm EGTM
                        Electric grid unit tariff multiplier
  -pvumc PVUMC, --pvumc PVUMC
                        Photovoltaics unit maintenance cost
  -wtumc WTUMC, --wtumc WTUMC
                        Wind turbine unit maintenance cost
  -deumc DEUMC, --deumc DEUMC
                        Diesel unit maintenance cost
  -btumc BTUMC, --btumc BTUMC
                        Battery unit maintenance cost
  -egumc EGUMC, --egumc EGUMC
                        Electric grid unit maintenance cost
  -deop DEOILPRICE, --deoilprice DEOILPRICE
                        Oil price. Be consistent with units of DE_RC
  -derc DERATECONSUMPTION, --derateconsumption DERATECONSUMPTION
                        Oil rate consumption. Be consistent with units of
                        DE_OP
  -demin DEMINPOWER, --deminpower DEMINPOWER
                        Min diesel power
  -demax DEMAXPOWER, --demaxpower DEMAXPOWER
                        Max diesel power
  -deru DERAMPUP, --derampup DERAMPUP
                        Diesel ramp up diesel
  -derd DERAMPDOWN, --derampdown DERAMPDOWN
                        Diesel ramp down diesel
  -demrt DEMINRUNNINGTIME, --deminrunningtime DEMINRUNNINGTIME
                        Diesel min running time
  -deaoc DEAOILCONSUMPTION, --deaoilconsumption DEAOILCONSUMPTION
                        Factor to model quadratic term in diesel consumtion
                        function
  -deboc DEBOILCONSUMPTION, --deboilconsumption DEBOILCONSUMPTION
                        Factor to model linear term in diesel consumtion
                        function
  -decoc DECOILCONSUMPTION, --decoilconsumption DECOILCONSUMPTION
                        Factor to model constant term in diesel consumtion
                        function
  -btsd BTSELFDIS, --btselfdis BTSELFDIS
                        Battery self discharge by operating cycle
  -btrc BTRATEDCAP, --btratedcap BTRATEDCAP
                        Battery rated capacity in kWh
  -btc BTC, --btc BTC   C factor to model battery behavior
  -btde BTDISCHARGEEFF, --btdischargeeff BTDISCHARGEEFF
                        Discharge efficiency in battery
  -btce BTCHARGEEFF, --btchargeeff BTCHARGEEFF
                        Charge efficiency in battery
  -btsmx BTSOCMAX, --btsocmax BTSOCMAX
                        Max SOC allowed in battery in percentage. Usually 100
  -btsmn BTSOCMIN, --btsocmin BTSOCMIN
                        Min SOC allowed in battery in percentage.
  -btsi BTSOCINIT, --btsocinit BTSOCINIT
                        Starting SOC for simulation.
  -ldws LDWEIGHTSAT, --ldweightsat LDWEIGHTSAT
                        Load weight factor of satisfaction.
  -ldb LDBETA, --ldbeta LDBETA
                        Factor to model satisfaction of load function
  -lda LDALPHA, --ldalpha LDALPHA
                        Factor to model satisfaction of load function
  -tn TESTNAME, --testname TESTNAME
                        Folder name to save tests to run
  -sa SAMPLESTOANALIZE, --samplestoanalize SAMPLESTOANALIZE
                        Number of units of time to analize
  -pg, --playwithgrid   Play with electric grid
  -ds DATASET, --dataset DATASET
                        Name of dataset for initial resources and load data

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
