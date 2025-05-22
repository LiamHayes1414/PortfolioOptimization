import random
import Calculations
import copy
import pandas as pd

#Data.Update_Training_Data()

#_Step 0: Collect data for training securities 
Samples = [
    "CNQ.TO","RY.TO","LNF.TO",
    "MKP.TO","BNS.TO","CLS.TO",
    "PBH.TO","HOD.TO","XIU.TO",
    "ZQQ.TO","CAP.PA","TTE.PA",
    "CA.PA","ALV.F","NESN.SW",
    "JPM","AAPL","O","IYJ",
    "XLE"
]
Calc_OBJ =Calculations.Calculate(Samples)
Portfolios = Calc_OBJ.Portfolios
Study_Range = Calc_OBJ.Study_Range

DATA = []

#_Step 3: Iterate through portfolios, generate random testing periods and collect features over test periods
for P in Portfolios:
    #n random performance periods
    n = 15
    Performance_Days = random.sample(Study_Range,n)

    for D in Performance_Days:

        #Result
        Perf = Calc_OBJ.Performance(D,P)

        #Specific Obj Instance
        Calc_Full = copy.deepcopy(Calc_OBJ)
        Calc_Short = copy.deepcopy(Calc_OBJ)
        
        Calc_Full.Specify(D,P,"Full")
        Calc_Short.Specify(D,P,"Short")

        #Features Full - Numerical
        with Calc_Full as calc:
            Er_Full = calc.ExpectedReturns().mean()
            STD_Full = calc.STD().mean()
            Beta_Full = calc.Beta().mean()
            Corr_Full = calc.Correlation().mean()
            TradingVol_Full = calc.TradingVol().mean()

        #Features Short - Numerical
        with Calc_Short as calc:
            Er_Short = calc.ExpectedReturns().mean()
            STD_Short = calc.STD().mean()
            Beta_Short = calc.Beta().mean()
            Corr_Short = calc.Correlation().mean()
            TradingVol_Short = calc.TradingVol().mean()


        Row = {
            "Er_F":Er_Full,
            "Er_S":Er_Short,
            "STD_F":STD_Full,
            "STD_S":STD_Short,
            "Beta_F":Beta_Full,
            "Beta_S":Beta_Short,
            "Corr_F":Corr_Full,
            "Corr_S":Corr_Short,
            "Vol_F":TradingVol_Full,
            "Vol_S":TradingVol_Short,

            "Perf":Perf
        }

        DATA.append(Row)


        #P/E_Full
        #P/E_Short
        #EPS_Full
        #EPS_Short
        #Inflation_Full
        #Inflation_Short
        #MarketCap_Full
        #MarketCap_Short
        #Profit_Full
        #Profit_Short
        #Revenue_Full
        #Revenue_Short
        #PrimeRate_Full
        #PrimeRate_Short
        #DisposableIncome

        #Features - Categorical


print(len(DATA))

TrainingSet = pd.DataFrame(DATA,index=False)
TrainingSet.to_csv("TrainingSet.csv")
