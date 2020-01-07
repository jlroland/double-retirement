import numpy as np
import pandas as pd

shill_data = pd.read_csv('data/shiller_monthly_data.csv', index_col=False)

refined_data = shill_data[['Date', 'Consumer Price Index CPI','Long Interest Rate GS10','Real Price', 'Real Dividend']]
print(refined_data.head())

#format date
#create column for inflation rate based on CPI


portfolio = 1000000                  #initial portfolio amount at retirement, using $1M as starting example
equity_portion = 0.5*portfolio       #50% of portfolio invested in S&P index
bond_portion = 0.5*portfolio         #50% of portfolio invested in 10-yr Treasury bonds
swr = 0.04                            #safe withdrawal rate, using 4% as starting example
portfolio = portfolio*(1-swr)          #withdraw funds for first year of retirement on Jan. 1

#portfolio = ((equity_portion)*market_delta + dividends) + (bond_portion*interest)