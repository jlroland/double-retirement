import numpy as np
import pandas as pd

shill_data = pd.read_csv('data/shiller_monthly_data.csv', index_col=False)

refined_data = shill_data[['Date', 'Consumer Price Index CPI','Long Interest Rate GS10','Real Price', 'Real Dividend']]

refined_data['Date'] = refined_data['Date'].map('{:.2f}'.format)
dec_cpi = refined_data['Consumer Price Index CPI'][[x.endswith('12') for x in refined_data['Date']]].reset_index()
print(dec_cpi)
jan_cpi = refined_data['Consumer Price Index CPI'][[x.endswith('01') for x in refined_data['Date']]].reset_index()
jan_cpi = jan_cpi[0:-1]       #removes Jan 2019 since Dec 2019 data not available
#print(jan_cpi)
annual_inflation = (dec_cpi-jan_cpi)/jan_cpi
#print(annual_inflation)
refined_data['Annual Inflation'] = 'NA'
refined_data['Annual Inflation'][[x.endswith('12') for x in refined_data['Date']]] = annual_inflation['Consumer Price Index CPI']
print(refined_data['Annual Inflation'][0:20])

#refined_data.info()
#create column for inflation rate based on CPI


portfolio = 1000000                  #initial portfolio amount at retirement, using $1M as starting example
equity_portion = 0.5*portfolio       #50% of portfolio invested in S&P index
bond_portion = 0.5*portfolio         #50% of portfolio invested in 10-yr Treasury bonds
swr = 0.04                            #safe withdrawal rate, using 4% as starting example
portfolio = portfolio*(1-swr)          #withdraw funds for first year of retirement on Jan. 1

#portfolio = ((equity_portion)*market_delta + dividends) + (bond_portion*interest)