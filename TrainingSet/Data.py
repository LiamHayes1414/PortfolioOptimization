import yfinance as yf
import pandas as pd


def Training_Data(Samples):

    #Indexes used for Beta
    IndexProxies = ['^GSPC','^DJI','^GSPTSE','^IXIC']

    #run through same generation processes for data cleanliness
    Info = Samples + IndexProxies

    Dividends = None
    Dataset = None
    Volume_Data = None
    for s in Info:
        Data = yf.Ticker(s).history(period="max")[['Close','Dividends','Volume']]

        Data.index = Data.index.strftime('%d-%m-%Y')

        #Non proxy data
        if s not in IndexProxies:
            #Dividends
            Div_Data = Data['Dividends'] 
            Div_Data.name = s
            if Dividends is None:
                Dividends = Div_Data.to_frame()
            else:
                Dividends = Dividends.join(Div_Data,how='outer')


            #Volume
            V_Data = Data['Volume']
            V_Data.name = s
            if Volume_Data is None:
                Volume_Data = V_Data.to_frame()
            else:
                Volume_Data = Volume_Data.join(V_Data,how='inner')


        df = Data['Close']
        df.name = s

        if Dataset is None:
            Dataset = df.to_frame()
        else:
            Dataset = Dataset.join(df,how='inner')

    #convert df index back to datetime obj for easier processing
    Dataset.index = pd.to_datetime(Dataset.index,format='%d-%m-%Y')
    Volume_Data.index = pd.to_datetime(Volume_Data.index,format='%d-%m-%Y')
    Dividends.index = pd.to_datetime(Dividends.index,format='%d-%m-%Y')

    StockData = Dataset[Samples]

    ProxyData = Dataset[IndexProxies]
    ProxyData = ProxyData.mean(axis=1)

    ProxyData.name = 'Proxy'

    return StockData,ProxyData,Dividends,Volume_Data


