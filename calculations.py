import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go


annual_data = pd.read_csv('data/shiller_annual_data.csv', index_col=False)

refined_data = annual_data[['Year', 'Consumer Price Index','Long Government Bond Yield','RealP Stock Price','RealD S&P Dividend', 'Return on S&P Composite']]
refined_data.drop(refined_data[refined_data['Year'] >= 2013].index, inplace=True)    #removed 2013 data since not all data is available
refined_data['Long Government Bond Yield'] = refined_data['Long Government Bond Yield']/100
refined_data['Annual Inflation'] = refined_data['Consumer Price Index'].pct_change().round(4)
refined_data['Annual Inflation'][0] = refined_data['Annual Inflation'][1]  #in absence of known rate, using following year's rate


def calculate_interest(principal, rate):
    '''
    Calculates bond interest compounded quarterly
    '''
    return principal*((1+rate/4)**4)

def calculate_portfolio(num_years, start_year, wr, pct_equity=0.5):
    '''
    Calculates ending portfolio balance over a given timeframe when starting with a balance of $100,000. The calculation is made using the specified annual withdrawal rate and specified asset allocation (default 50/50 equities/fixed income).
    
    Parameters:
    num_years (int): length of retirement period
    start_year (int): historical calendar year in which retirement period starts
    wr (float): initial withdrawal rate
    pct_equity (float): percent of portfolio invested in equities, default=0.5

    Returns:
    portfolio (float): ending portfolio balance in dollars

    '''
    init_portfolio = 100000
    withdrawal_amount = init_portfolio*wr
    year1_balance = init_portfolio-withdrawal_amount
    equity_portion = pct_equity*year1_balance 
    bond_portion = (1-pct_equity)*year1_balance
    
    for i in range(start_year, start_year+num_years-1):
        num_shares = equity_portion/refined_data['RealP Stock Price'][i]
        portfolio = (equity_portion*(1+refined_data['Return on S&P Composite'][i]) + num_shares*refined_data['RealD S&P Dividend'][i]) + calculate_interest(bond_portion, refined_data['Long Government Bond Yield'][i])
        withdrawal_amount += withdrawal_amount*refined_data['Annual Inflation'][i]
        portfolio -= withdrawal_amount
        equity_portion = pct_equity*portfolio    #rebalance asset allocation each year
        bond_portion = (1-pct_equity)*portfolio
    return portfolio

def prob_success(num_years, wr):
    '''
    Calculates the probability of portfolio success based on historical data for a specified retirement length and initial withdrawal rate; portfolio success is defined as an ending portfolio balance greater than zero. 

    Parameters:
    num_years (int): length of retirement period
    wr (float): initial withdrawal rate

    Returns:
    probability of success (float): probability of ending portfolio balance >0, based on past observations
    
    '''
    success = 0
    for i in range(0,142-num_years):
        result = calculate_portfolio(num_years, i, wr)
        if result > 0:
            success += 1
    return success/(142-num_years)

retire_length = np.arange(30, 61, 10)
wr_list = np.linspace(0, 0.1, 21)

num_years_dict = {"prob{}".format(val): (val, []) for i, val in enumerate(retire_length)}
for i in range(len(wr_list)):
    for k,v in sorted(num_years_dict.items()):
        num_years_dict[k][1].append(prob_success(num_years_dict[k][0], wr_list[i]))
        
years_30 = np.arange(0,112)
end_balance_30 = []
years_60 = np.arange(0,82)
end_balance_60 = []
for i in range(len(years_30)):
    end_balance_30.append(calculate_portfolio(30, years_30[i], 0.04))
for i in range(len(years_60)):
    end_balance_60.append(calculate_portfolio(60, years_60[i], 0.04))

fig = make_subplots(rows=1, cols=2, subplot_titles=('Ending Portfolio Balance (Starting Balance = $100K)', 'Probability of Success'))
fig.add_trace(go.Scatter(x=refined_data['Year'][0:112], y=end_balance_30, name='30-year retirement'), row=1, col=1)
fig.add_trace(go.Scatter(x=refined_data['Year'][0:112], y=end_balance_60, name='60-yr retirement'), row=1, col=1)
fig.add_trace(go.Scatter(x=wr_list, y=num_years_dict['prob30'][1], name='30-yr retirement', line=dict(color='royalblue', width=3, dash='dot')), row=1, col=2)
fig.add_trace(go.Scatter(x=wr_list, y=num_years_dict['prob40'][1], name='40-yr retirement', line=dict(color='green', width=3, dash='dot')), row=1, col=2)
fig.add_trace(go.Scatter(x=wr_list, y=num_years_dict['prob50'][1], name='50-yr retirement', line=dict(color='orange', width=3, dash='dot')), row=1, col=2)
fig.add_trace(go.Scatter(x=wr_list, y=num_years_dict['prob60'][1], name='60-yr retirement', line=dict(color='red', width=3, dash='dot')), row=1, col=2)
fig.update_xaxes(title_text='Year Retirement Began', nticks=10, row=1, col=1)
fig.update_yaxes(title_text='Ending Portfolio Balance', row=1, col=1)
fig.update_xaxes(title_text='Initial Withdrawal Rate', row=1, col=2)
fig.update_yaxes(title_text='Probability of Success', row=1, col=2)
fig.update_layout(title='Analysis Based on Historical Investment Returns')

fig.show()
#fig.write_image('images/portfolio_success_historical_4pct.png', width=1000, height=500)
