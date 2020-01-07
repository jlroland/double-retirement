%matplotlib inline
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('ggplot')

shill_data = pd.read_csv('data/shiller_monthly_data.csv', index_col=False)

refined_data = shill_data[['Date', 'Consumer Price Index CPI','Long Interest Rate GS10','Real Price', 'Real Dividend']]
refined_data.drop(refined_data[refined_data['Date'] >= 2019].index, inplace=True)    #removed 2019 data since full year not available
refined_data['Date'] = pd.to_numeric(refined_data['Date']).map('{:.2f}'.format)
refined_data['Long Interest Rate GS10'] = refined_data['Long Interest Rate GS10']/100

dec_data = refined_data[[x.endswith('12') for x in refined_data['Date']]].reset_index()
jan_data = refined_data[[x.endswith('01') for x in refined_data['Date']]].reset_index()

dec_data['Annual Inflation'] = ((dec_data['Consumer Price Index CPI']-jan_data['Consumer Price Index CPI'])/jan_data['Consumer Price Index CPI']).round(4)
#dec_data
#stretch goal -- create column in refined_data for monthly inflation rate based on CPI

dec_data['Annual Gain/Loss'] = ((dec_data['Real Price']-jan_data['Real Price'])/jan_data['Real Price']).round(4)
#dec_data
#stretch goal -- create column in refined_data for monthly gain/loss



init_portfolio = 1000000                  #initial portfolio amount at retirement, using $1M as starting example    
swr = 0.04                            #safe withdrawal rate, using 4% as starting example
year1_balance = init_portfolio*(1-swr)          #withdraw funds for first year of retirement on Jan. 1
equity_portion = 0.5*year1_balance       #50% of portfolio invested in S&P index
bond_portion = 0.5*year1_balance         #50% of portfolio invested in 10-yr Treasury bonds

fig, ax = plt.subplots()
for i in range(59):
    num_shares = equity_portion/dec_data['Real Price'][i]
    portfolio = (equity_portion*(1+dec_data['Annual Gain/Loss'][i]) + num_shares*dec_data['Real Dividend'][i]) + (bond_portion*(1+dec_data['Long Interest Rate GS10'][i]))
    portfolio = portfolio*(1-(swr*(1+dec_data['Annual Inflation'][i])))
    equity_portion = 0.5*portfolio
    bond_portion = 0.5*portfolio
    ax.scatter(i, portfolio)







