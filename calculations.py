%matplotlib inline
import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
plt.style.use('ggplot')

shill_data = pd.read_csv('data/shiller_monthly_data.csv', index_col=False)

refined_data = shill_data[['Date', 'Consumer Price Index CPI','Long Interest Rate GS10','Real Price', 'Real Dividend']]
refined_data.drop(refined_data[refined_data['Date'] >= 2019].index, inplace=True)    #removed 2019 data since full year not available
refined_data['Date'] = pd.to_numeric(refined_data['Date']).map('{:.2f}'.format)
refined_data['Long Interest Rate GS10'] = refined_data['Long Interest Rate GS10']/100

dec_data = refined_data[[x.endswith('12') for x in refined_data['Date']]].reset_index()
jan_data = refined_data[[x.endswith('01') for x in refined_data['Date']]].reset_index()

dec_data['Annual Inflation'] = dec_data['Consumer Price Index CPI'].pct_change().round(4)
dec_data['Annual Inflation'][0] = ((dec_data['Consumer Price Index CPI'][0]-jan_data['Consumer Price Index CPI'][0])/jan_data['Consumer Price Index CPI'][0]).round(4)

#stretch goal -- create column in refined_data for monthly inflation rate based on CPI

dec_data['Annual Gain/Loss'] = dec_data['Real Price'].pct_change().round(4)
dec_data['Annual Gain/Loss'][0] = ((dec_data['Real Price'][0]-jan_data['Real Price'][0])/jan_data['Real Price'][0]).round(4)

#stretch goal -- create column in refined_data for monthly gain/loss

#quarterly compounding of bond interest
def calculate_interest(principal, rate):
    return principal*((1+rate/4)**4)

#start with traditional 30-yr for comparison
def calculate_30(start_year, wr, pct_equity=0.5):
    port_values = []
    init_portfolio = 1000000
    port_values.append(init_portfolio)
    withdrawal_amount = init_portfolio*wr
    year1_balance = init_portfolio-withdrawal_amount
    equity_portion = pct_equity*year1_balance 
    bond_portion = (1-pct_equity)*year1_balance
    
    for i in range(start_year, start_year+29):
        num_shares = equity_portion/dec_data['Real Price'][i]
        portfolio = (equity_portion*(1+dec_data['Annual Gain/Loss'][i]) + num_shares*dec_data['Real Dividend'][i]) + calculate_interest(bond_portion, dec_data['Long Interest Rate GS10'][i])
        withdrawal_amount += withdrawal_amount*dec_data['Annual Inflation'][i]
        portfolio -= withdrawal_amount
        port_values.append(portfolio)
        equity_portion = pct_equity*portfolio
        bond_portion = (1-pct_equity)*portfolio
    return portfolio

def calculate_60(start_year, wr, pct_equity=0.5):
    port_values = []
    init_portfolio = 1000000
    port_values.append(init_portfolio)
    withdrawal_amount = init_portfolio*wr
    year1_balance = init_portfolio-withdrawal_amount 
    equity_portion = pct_equity*year1_balance 
    bond_portion = (1-pct_equity)*year1_balance
    
    for i in range(start_year, start_year+59):
        num_shares = equity_portion/dec_data['Real Price'][i]
        portfolio = (equity_portion*(1+dec_data['Annual Gain/Loss'][i]) + num_shares*dec_data['Real Dividend'][i]) + calculate_interest(bond_portion, dec_data['Long Interest Rate GS10'][i])
        withdrawal_amount += withdrawal_amount*dec_data['Annual Inflation'][i]
        portfolio -= withdrawal_amount
        port_values.append(portfolio)
        equity_portion = pct_equity*portfolio
        bond_portion = (1-pct_equity)*portfolio
    return portfolio

def prob_success_30(wr):
    success = 0
    for i in range(0,120):
        result = calculate_30(i, wr)
        if result > 0:
            success += 1
    return success/120

def prob_success_60(wr):
    success = 0
    for i in range(0,90):
        result = calculate_60(i, wr)
        if result > 0:
            success += 1
    return success/90

wr_list = np.linspace(0, 0.1, 21)
prob_30 = []
prob_60 = []
for i in range(len(wr_list)):
    prob_30.append(prob_success_30(wr_list[i]))
    prob_60.append(prob_success_60(wr_list[i]))

years_30 = np.arange(0,120)
end_balance_30 = []
years_60 = np.arange(0,90)
end_balance_60 = []
for i in range(len(years_30)):
    end_balance_30.append(calculate_30(years_30[i], 0.04))
for i in range(len(years_60)):
    end_balance_60.append(calculate_60(years_60[i], 0.04))
    
fig = make_subplots(rows=1, cols=2, subplot_titles=('Ending Portfolio Balance (Starting Balance = $1M)', 'Probability of Success'))
fig.add_trace(go.Scatter(x=years30, y=end_balance_30, name='30-year retirement'), row=1, col=1)
fig.add_trace(go.Scatter(x=years60, y=end_balance_60, name='60-yr retirement'), row=1, col=1)
fig.add_trace(go.Scatter(x=wr_list, y=prob_30, name='30-yr retirement'), row=1, col=2)
fig.add_trace(go.Scatter(x=wr_list, y=prob_60, name='60-yr retirement'), row=1, col=2)
fig.update_xaxes(title_text='Year Retirement Began', row=1, col=1)
fig.update_yaxes(title_text='Ending Portfolio Balance', row=1, col=1)
fig.update_xaxes(title_text='Initial Withdrawal Rate', row=1, col=2)
fig.update_yaxes(title_text='Probability of Success', row=1, col=2)

fig.show()
#fig.write_image('portfolio_success_4pct.png')



#refined_data['Monthly Inflation'] = refined_data['Consumer Price Index CPI'].pct_change()
#refined_data['Monthly Gain/Loss'] = refined_data['Real Price'].pct_change()


#monthly evaluation & withdrawal
# def calculate_30(start_date, wr):
#     port_values = []
#     init_portfolio = 1000000
#     port_values.append(init_portfolio)
#     withdrawal_amount = (init_portfolio*wr)/12
#     month2_balance = init_portfolio-withdrawal_amount
#     equity_portion = 0.5*month2_balance 
#     bond_portion = 0.5*month2_balance
    
#     for i in range(start_date, start_date+359):
#         num_shares = equity_portion/refined_data['Real Price'][i]
#         portfolio = equity_portion*(1+refined_data['Monthly Gain/Loss'][i]) + num_shares*(refined_data['Real Dividend'][i]/12) + calculate_interest(bond_portion, refined_data['Long Interest Rate GS10'][i]/12)
#         withdrawal_amount += withdrawal_amount*refined_data['Monthly Inflation'][i]
#         portfolio -= withdrawal_amount
#         port_values.append(portfolio)
#         equity_portion = 0.5*portfolio
#         bond_portion = 0.5*portfolio
#     return portfolio
