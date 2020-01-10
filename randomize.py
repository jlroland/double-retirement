import numpy as np
import pandas as pd
from statistics import mean
from plotly.subplots import make_subplots
import plotly.graph_objects as go


def get_random_data():
    sample1 = random.triangular(-0.5, 0, -0.05)
    sample2 = random.triangular(0, 0.5, 0.1)
    sample_set = random.choice([sample1,sample2])
    rand_returns = [0.0515]

    for i in range(147):
        rand_returns.append(random.choice([random.triangular(-0.5, 0, -0.05),random.triangular(0, 0.5, 0.1)]))

    rand_price = [96.32]
    for i in range(1,len(rand_returns)):
        rand_price.append(rand_price[i-1]*(1+rand_returns[i]))

    rand_returns = np.around(np.array(rand_returns),4)
    rand_price = np.array(rand_price)
    return rand_price,rand_returns

def calculate_rand_portfolio(num_years, start_year, wr, pct_equity=0.5):
    init_portfolio = 1000000
    withdrawal_amount = init_portfolio*wr
    year1_balance = init_portfolio-withdrawal_amount
    equity_portion = pct_equity*year1_balance 
    bond_portion = (1-pct_equity)*year1_balance
    rand_data = get_random_data()
    
    for i in range(start_year, start_year+num_years-1):
        num_shares = equity_portion/rand_data[0][i]
        portfolio = (equity_portion*(1+rand_data[1][i]) + num_shares*dec_data['Real Dividend'][i]) + calculate_interest(bond_portion, dec_data['Long Interest Rate GS10'][i])
        withdrawal_amount += withdrawal_amount*dec_data['Annual Inflation'][i]
        portfolio -= withdrawal_amount
        equity_portion = pct_equity*portfolio    #rebalance asset allocation each year
        bond_portion = (1-pct_equity)*portfolio
    return portfolio

def prob_rand_success(num_years, wr):
    success = 0
    for i in range(0,150-num_years):
        result = calculate_rand_portfolio(num_years, i, wr)
        if result > 0:
            success += 1
    return success/(150-num_years)

fig = go.Figure()
prob_rand_30 = []
prob_rand_60 = []
for i in range(100):
    prob_rand_30.append(prob_rand_success(30, 0.04))
    prob_rand_60.append(prob_rand_success(60, 0.04))
fig.add_trace(go.Scatter(x=np.arange(100), y=prob_rand_30, mode='markers', name='30-yr random'))
fig.add_trace(go.Scatter(x=np.arange(100), y=prob_rand_60, mode='markers', name='60-yr random'))
fig.add_shape(
        go.layout.Shape(type="line", x0=0, y0=mean(prob_rand_30), x1=100, y1=mean(prob_rand_30), line=dict(
                color="RoyalBlue",
                width=3
            )))
fig.add_shape(
        go.layout.Shape(type="line", x0=0, y0=mean(prob_rand_60), x1=100, y1=mean(prob_rand_60), line=dict(
                color="Red",
                width=3
            )))
fig.show()
#fig.write_image('portfolio_success_random_4pct.png')

fig = go.Figure()
prob_rand_30_3 = []
prob_rand_60_3 = []
for i in range(100):
    prob_rand_30_3.append(prob_rand_success(30, 0.03))
    prob_rand_60_3.append(prob_rand_success(60, 0.03))
fig.add_trace(go.Scatter(x=np.arange(100), y=prob_rand_30_3, mode='markers', name='30-yr random'))
fig.add_trace(go.Scatter(x=np.arange(100), y=prob_rand_60_3, mode='markers', name='60-yr random'))
fig.add_shape(
        go.layout.Shape(type="line", x0=0, y0=mean(prob_rand_30_3), x1=100, y1=mean(prob_rand_30_3), line=dict(
                color="RoyalBlue",
                width=3
            )))
fig.add_shape(
        go.layout.Shape(type="line", x0=0, y0=mean(prob_rand_60_3), x1=100, y1=mean(prob_rand_60_3), line=dict(
                color="Red",
                width=3
            )))
fig.show()
#fig.write_image('portfolio_success_random_3pct.png')