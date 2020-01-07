import numpy as np
import pandas as pd

shill_data = pd.read_csv('data/shiller_monthly_data.csv', index_col=False)

refined_data = shill_data[['Date', 'Consumer Price Index CPI','Long Interest Rate GS10','Real Price', 'Real Dividend']]

refined_data['Date'] = pd.to_numeric(refined_data['Date']).map('{:.2f}'.format)
refined_data.drop(refined_data[refined_data['Date'] >= 2019].index, inplace=True)    #removed 2019 data since full year not available
                              
dec_cpi = refined_data['Consumer Price Index CPI'][[x.endswith('12') for x in refined_data['Date']]].reset_index()
#print(dec_cpi)
jan_cpi = refined_data['Consumer Price Index CPI'][[x.endswith('01') for x in refined_data['Date']]].reset_index()
#print(jan_cpi)
annual_inflation = (dec_cpi-jan_cpi)/jan_cpi
#print(annual_inflation)

refined_data['Annual Inflation'] = 'NA'
for i in range(len(dec_cpi)):
    refined_data['Annual Inflation'][dec_cpi['index'][i]] = annual_inflation['Consumer Price Index CPI'][i]

#stretch goal -- create column for monthly inflation rate based on CPI

dec_price = refined_data['Real Price'][[x.endswith('12') for x in refined_data['Date']]].reset_index()

jan_price = refined_data['Real Price'][[x.endswith('01') for x in refined_data['Date']]].reset_index()

annual_delta = (dec_price-jan_price)/jan_price

refined_data['Annual Gain/Loss'] = 'NA'
for i in range(len(dec_price)):
    refined_data['Annual Gain/Loss'][dec_price['index'][i]] = annual_delta['Real Price'][i]

#stretch goal -- create column for monthly gain/loss

portfolio = 1000000                  #initial portfolio amount at retirement, using $1M as starting example
equity_portion = 0.5*portfolio       #50% of portfolio invested in S&P index
bond_portion = 0.5*portfolio         #50% of portfolio invested in 10-yr Treasury bonds
swr = 0.04                            #safe withdrawal rate, using 4% as starting example
portfolio = portfolio*(1-swr)          #withdraw funds for first year of retirement on Jan. 1

#portfolio = ((equity_portion)*market_delta + dividends) + (bond_portion*interest)






