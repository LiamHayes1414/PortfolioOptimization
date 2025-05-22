from TrainingSet import Data
import autograd.numpy as np
from dateutil.relativedelta import relativedelta
from itertools import combinations

class Calculate:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __init__(self,Samples):
        self.Samples = Samples
        self.Dataset,self.Proxy,self.Dividends,self.Volume = Data.Training_Data(self.Samples)

        #Generate range to track performance over
        Date_Range = self.Dataset.index.tolist()

        #Buffer so there will be at least 'Cutoff' number of days to collect historical performance
        Cutoff = 1500
        self.Study_Range = Date_Range[Cutoff:] 

        #Generate portfolio combinations for security list
        self.Portfolios = list(combinations(Samples, 4))

        #Period & Portfolio specific Data
        self.Price_Data = None
        self.Dividend_Data = None
        self.Volume_Data = None

    def Specify(self,Date,Portfolio,Type):
        TrainingDataEnd = Date - relativedelta(years = 1) #Last date available for training range (from TrainingDataEnd to Date is range for testing unknown performance)
        ShortTrainingStart = TrainingDataEnd - relativedelta(years = 1) 

        #Filter for specific portfolio
        DataP = self.Dataset[list(Portfolio)]
        DataD = self.Dividends[list(Portfolio)]
        DataV = self.Volume[list(Portfolio)]

        #Filter Date by specified study range
        if Type == "Full":
            self.Price_Data = DataP[(DataP.index <= TrainingDataEnd)]
            self.Dividend_Data = DataD[(DataD.index <= TrainingDataEnd)]
            self.Volume_Data = DataV[(DataV.index <= TrainingDataEnd)]
        elif Type == "Short":
            self.Price_Data = DataP[(DataP.index <= TrainingDataEnd) & (DataP.index >=ShortTrainingStart)]
            self.Dividend_Data = DataD[(DataD.index <= TrainingDataEnd) & (DataD.index >=ShortTrainingStart)] 
            self.Volume_Data = DataV[(DataV.index <= TrainingDataEnd) & (DataV.index >=ShortTrainingStart)]
            
        else:
            raise ValueError("Type must either be 'Full' or 'Short'")

    def Performance(self,End_Date,Portfolio):
        #Calculate performance of portfolio over given period (result column in end training set)

        #study range
        Start_Date = End_Date - relativedelta(years=1)
        Portf_Data = self.Dataset[list(Portfolio)]
        df = Portf_Data[(Portf_Data.index >= Start_Date)&(Portf_Data.index <= End_Date)]

        #Capital yield
        pct_chng = (((df.iloc[-1] - df.iloc[0])/df.iloc[0]).mean())

        #Dividend yield
        Dividend_Data = self.Dividends[list(Portfolio)]
        Dividend_Data = Dividend_Data[(Dividend_Data.index <= End_Date) & (Dividend_Data.index >=Start_Date)] 
        Total_Dividends = Dividend_Data.sum().sum()

        DivPct = Total_Dividends/sum(df.iloc[0])

        return pct_chng + DivPct

    def ExpectedReturns(self):

        #Calculate average daily %return and annualize
        AvgDailyReturn= self.Price_Data.pct_change().mean()
        AnnualReturn = ((1+AvgDailyReturn)**252) -1

        #Dividend Yield
        Div_Returns = self.Dividend_Data.sum()/self.Price_Data.mean()

        return (AnnualReturn + Div_Returns).to_numpy()
            
    def STD(self):   
        #Standard deviation of %change from one day to the next
        DailySTD = self.Price_Data.pct_change().std()
        AnnualSTD = DailySTD * np.sqrt(252) #<- annualize daily std

        return AnnualSTD.to_numpy()

    def Beta(self):
        B_Vector = np.array([])

        All = self.Price_Data.join(self.Proxy,how='inner').pct_change().dropna()

        Portfolio = All.drop(columns=['Proxy'])
        Market = All['Proxy']

        MarketVariance = np.var(Market)

        for Stock, Data in Portfolio.items():
            CoVariance = np.cov(Market,Data)[0,1]
            Beta = CoVariance/MarketVariance

            B_Vector = np.append(B_Vector,Beta)

        return B_Vector

    def Correlation(self):
        Securities = list(self.Price_Data.columns)
        C_Vector = np.array([])
        S_Pairs = list(combinations(Securities, 2))

        for pair in S_Pairs:
            Correlation = self.Price_Data[pair[0]].corr(self.Price_Data[pair[1]])
            C_Vector= np.append(C_Vector,Correlation)

        return C_Vector
    
    def TradingVol(self):
        Volume = self.Volume_Data.mean().to_numpy()
 

        return Volume

    def Inflation(self):
        # US https://www.bls.gov/developers/
        # Canada https://www.statcan.gc.ca/en/developers
        # UK https://developer.ons.gov.uk/

        print("Hello")
