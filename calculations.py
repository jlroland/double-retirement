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

#start with traditional 30-yr for comparison
def calculate_30(start, wr, ax):
    port_values = []
    init_portfolio = 1000000
    port_values.append(init_portfolio)
    withdrawal = init_portfolio*wr
    year1_balance = init_portfolio-withdrawal
    equity_portion = 0.5*year1_balance 
    bond_portion = 0.5*year1_balance
    
    for i in range(start, start+29):
        num_shares = equity_portion/dec_data['Real Price'][i]
        portfolio = (equity_portion*(1+dec_data['Annual Gain/Loss'][i]) + num_shares*dec_data['Real Dividend'][i]) + (bond_portion*(1+dec_data['Long Interest Rate GS10'][i]))
        withdrawal += withdrawal*dec_data['Annual Inflation'][i]
        portfolio -= withdrawal
        port_values.append(portfolio)
        equity_portion = 0.5*portfolio
        bond_portion = 0.5*portfolio
    ax.plot(range(start-1,start+29), port_values)
    return portfolio

def calculate_60(start, wr, ax):
    port_values = []
    init_portfolio = 1000000
    port_values.append(init_portfolio)
    withdrawal = init_portfolio*wr
    year1_balance = init_portfolio-withdrawal 
    equity_portion = 0.5*year1_balance 
    bond_portion = 0.5*year1_balance
    
    for i in range(start, start+59):
        num_shares = equity_portion/dec_data['Real Price'][i]
        portfolio = (equity_portion*(1+dec_data['Annual Gain/Loss'][i]) + num_shares*dec_data['Real Dividend'][i]) + (bond_portion*(1+dec_data['Long Interest Rate GS10'][i]))
        withdrawal += withdrawal*dec_data['Annual Inflation'][i]
        portfolio -= withdrawal
        port_values.append(portfolio)
        equity_portion = 0.5*portfolio
        bond_portion = 0.5*portfolio
    ax.plot(range(start-1,start+59), port_values)
    return portfolio

fig, ax = plt.subplots()
success30 = 0
failure30 = 0


for i in range(1,120):
    result30 = calculate_30(i, 0.04, ax)
    if result30 > 0:
        success30 += 1
    elif result30 <= 0:
        failure30 +=1
print(success30, failure30)

fig, ax = plt.subplots()
success60 = 0
failure60 = 0
for i in range(1,90):
    result = calculate_60(i, 0.04, ax)
    if result > 0:
        success60 += 1
    elif result <= 0:
        failure60 +=1
print(success60, failure60)




