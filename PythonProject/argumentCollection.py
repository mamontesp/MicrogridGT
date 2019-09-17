import io
import argparse
import sys
import re

def ParsingArguments():
    #Default Values
    ALPHA = 0.1 						# Weight of power balance
    POWERBALANCE = 2								# Update of alpha in case power balance is not reached
    NASHEQUILIBRIUM = 4								# Update of alpha in case nash equilibrium is not reached

    #unit_electric_price
    PV_UEP = 2.0
    WT_UEP = 4.0
    DE_UEP = 4.0
    BT_UEP = 0.1
    LD_UEP = 0.4
    EG_TM = 20

    #unit_maintenance_cost
    PV_UMC = 0.5
    WT_UMC = 3.0
    DE_UMC = 3.0
    BT_UMC = 0.05
    EG_UMC = 0.02

    #Diesel
    DE_OP = 3.0							#oil_price
    DE_RC = 2							#rate consumption
    DE_MIN = 0							#min diesel power
    DE_MAX = 10							#max diesel power
    DE_RAMP_UP = 1						#Ramp up for diesel machine
    DE_RAMP_DOWN = 3    				#Ramp down for diesel machine
    DE_MIN_RUNNING_TIME = 0.3			#Diesel machine min running time
    
    #diesel consumption arguments
    DE_A_OIL_CONSUMPTION = 1
    DE_B_OIL_CONSUMPTION = 2
    DE_C_OIL_CONSUMPTION = 1

    #Battery 
    BT_SELF_DIS = 0.0000001				#Self discharge rate
    BT_RATED_CAP = 5					#Rated Capacity
    BT_C = 0.2							#Battery C
    BT_DIS_EFF = 0.99					#Battery discharging efficiency
    BT_CHAR_EFF = 0.99					#Battery charging efficiency
    BT_SOC_MAX = 100					#Battery SOC max
    BT_SOC_MIN = 60						#Battery SOC min
    BT_SOC_INIT = 70					#Battery SOC init

    #Load
    LD_WEIGHT_SAT = 0.9
    LD_BETA = -1
    LD_ALPHA = 0.5
    
    TEST_NAME = 'Test'
    SAMPLES_TO_ANALIZE = 20
    DATA_SET_FILE_NAME = '../FormattedDataSets/dataWithoutBatteries.csv'

    Parser = argparse.ArgumentParser(description='Renewable resources dispatch')
    Parser.add_argument("-a","--alpha",help="Weight of power balance",default=ALPHA)
    Parser.add_argument("-d1", "--powerbalance", help="Update of alpha in case power balance is not reached", default=POWERBALANCE)
    Parser.add_argument("-d2", "--nashequilibrium", help="Update of alpha in case nash equilibrium is not reached", default=NASHEQUILIBRIUM)
    
    Parser.add_argument("-pvuep","--pvuep",help="Photovoltaics unit electric price",default=PV_UEP)
    Parser.add_argument("-wtuep","--wtuep",help="Wind turbine unit electric price",default=WT_UEP)
    Parser.add_argument("-deuep","--deuep",help="Diesel unit electric price",default=DE_UEP)
    Parser.add_argument("-btuep","--btuep",help="Battery unit electric price",default=BT_UEP)
    Parser.add_argument("-lduep","--lduep",help="Load unit electric price",default=LD_UEP)
    Parser.add_argument("-egtm","--egtm",help="Electric grid unit tariff multiplier",default=EG_TM)

    Parser.add_argument("-pvumc","--pvumc",help="Photovoltaics unit maintenance cost",default=PV_UMC)
    Parser.add_argument("-wtumc","--wtumc",help="Wind turbine unit maintenance cost",default=WT_UMC)
    Parser.add_argument("-deumc","--deumc",help="Diesel unit maintenance cost",default=DE_UMC)
    Parser.add_argument("-btumc","--btumc",help="Battery unit maintenance cost",default=BT_UMC)
    Parser.add_argument("-egumc","--egumc",help="Electric grid unit maintenance cost",default=EG_UMC)

    Parser.add_argument("-deop","--deoilprice",help="Oil price. Be consistent with units of DE_RC",default=DE_OP)
    Parser.add_argument("-derc","--derateconsumption",help="Oil rate consumption. Be consistent with units of DE_OP",default=DE_RC)
    Parser.add_argument("-demin","--deminpower",help="Min diesel power",default=DE_MIN)
    Parser.add_argument("-demax","--demaxpower",help="Max diesel power",default=DE_MAX)
    Parser.add_argument("-deru","--derampup",help="Diesel ramp up diesel",default=DE_RAMP_UP)
    Parser.add_argument("-derd","--derampdown",help="Diesel ramp down diesel",default=DE_RAMP_DOWN)
    Parser.add_argument("-demrt","--deminrunningtime",help="Diesel min running time",default=DE_MIN_RUNNING_TIME)
    Parser.add_argument("-deaoc","--deaoilconsumption",help="Factor to model quadratic term in diesel consumtion function",default=DE_A_OIL_CONSUMPTION)
    Parser.add_argument("-deboc","--deboilconsumption",help="Factor to model linear term in diesel consumtion function",default=DE_B_OIL_CONSUMPTION)
    Parser.add_argument("-decoc","--decoilconsumption",help="Factor to model constant term in diesel consumtion function",default=DE_C_OIL_CONSUMPTION)

    Parser.add_argument("-btsd","--btselfdis",help="Battery self discharge by operating cycle",default=BT_SELF_DIS)
    Parser.add_argument("-btrc","--btratedcap",help="Battery rated capacity in kWh",default=BT_RATED_CAP)
    Parser.add_argument("-btc","--btc",help="C factor to model battery behavior",default=BT_C)
    Parser.add_argument("-btde","--btdischargeeff",help="Discharge efficiency in battery",default=BT_DIS_EFF)
    Parser.add_argument("-btce","--btchargeeff",help="Charge efficiency in battery",default=BT_CHAR_EFF)
    Parser.add_argument("-btsmx","--btsocmax",help="Max SOC allowed in battery in percentage. Usually 100",default=BT_SOC_MAX)
    Parser.add_argument("-btsmn","--btsocmin",help="Min SOC allowed in battery in percentage.",default=BT_SOC_MIN)
    Parser.add_argument("-btsi","--btsocinit",help="Starting SOC for simulation.",default=BT_SOC_INIT)

    Parser.add_argument("-ldws","--ldweightsat",help="Load weight factor of satisfaction.",default=LD_WEIGHT_SAT)
    Parser.add_argument("-ldb","--ldbeta",help="Factor to model satisfaction of load function",default=LD_BETA)
    Parser.add_argument("-lda","--ldalpha",help="Factor to model satisfaction of load function",default=LD_ALPHA)

    Parser.add_argument("-tn","--testname",help="Folder name to save tests to run",default=TEST_NAME)
    Parser.add_argument("-sa","--samplestoanalize",help="Number of units of time to analize",default=SAMPLES_TO_ANALIZE)
        
    Parser.add_argument("-pg", "--playwithgrid", help="Option to include player electric grid to the game", action="store_true", default=False)
    Parser.add_argument("-ds", "--dataset", help="Name of dataset for initial resources and load data", default = DATA_SET_FILE_NAME)

    Args=Parser.parse_args()
    return Args



