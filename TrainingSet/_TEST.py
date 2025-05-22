import yfinance as yf
import pandas as pd
import requests


Samples = [
    "CNQ.TO","RY.TO","LNF.TO",
    "MKP.TO","BNS.TO","CLS.TO",
    "PBH.TO","HOD.TO","XIU.TO",
    "ZQQ.TO","CAP.PA","TTE.PA",
    "CA.PA","ALV.F","NESN.SW",
    "JPM","AAPL","O","IYJ",
    "XLE"
]

#for s in Samples:
    #ticker = yf.Ticker(s)
    #print(ticker.info['currency'])

id = "1810000401"
url = f"https://www150.statcan.gc.ca/t1/wds/rest/getFullTableDownloadCSV/{id}/en"

response = requests.get(url)

print(response.json())


