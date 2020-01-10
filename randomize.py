import numpy as np
import pandas as pd
import random
from statistics import mean
from plotly.subplots import make_subplots
import plotly.graph_objects as go

annual_data = pd.read_csv('data/shiller_annual_data.csv', index_col=False)

refined_data = annual_data[['Year', 'Consumer Price Index','Long Government Bond Yield','RealP Stock Price','RealD S&P Dividend', 'Return on S&P Composite']]
refined_data.drop(refined_data[refined_data['Year'] >= 2013].index, inplace=True)    #removed 2013 data since not all data is available
refined_data['Long Government Bond Yield'] = refined_data['Long Government Bond Yield']/100
refined_data['Annual Inflation'] = refined_data['Consumer Price Index'].pct_change().round(4)
refined_data['Annual Inflation'][0] = refined_data['Annual Inflation'][1]  #in absence of known rate, using following year's rate

fig = go.Figure(data=[go.Histogram(x=refined_data['Return on S&P Composite'])])
fig.update_layout(
    title_text='Frequency of S&P Returns',
    xaxis_title_text='Percent Return',
    yaxis_title_text='Count'
)
fig.show()
#fig.write_image('images/annual_returns_frequency.png')

def get_random_data():
    rand_returns = []

    for i in range(142):
        rand_returns.append(random.choice([random.triangular(-0.5, 0.075, 0.025),random.triangular(0.075, 0.5, 0.125)]))

    rand_price = [82.03]
    for i in range(len(rand_returns)-1):
        rand_price.append(rand_price[i]*(1+rand_returns[i]))

    rand_returns = np.around(np.array(rand_returns),4)
    rand_price = np.array(rand_price)
    return rand_price,rand_returns

#calculates bond interest compounded quarterly
def calculate_interest(principal, rate):
    return principal*((1+rate/4)**4)

def calculate_rand_portfolio(num_years, start_year, wr, pct_equity=0.5):
    init_portfolio = 100000
    withdrawal_amount = init_portfolio*wr
    year1_balance = init_portfolio-withdrawal_amount
    equity_portion = pct_equity*year1_balance 
    bond_portion = (1-pct_equity)*year1_balance
    rand_data = get_random_data()
    
    for i in range(start_year, start_year+num_years-1):
        num_shares = equity_portion/rand_data[0][i]
        portfolio = (equity_portion*(1+rand_data[1][i]) + num_shares*refined_data['RealD S&P Dividend'][i]) + calculate_interest(bond_portion, refined_data['Long Government Bond Yield'][i])
        withdrawal_amount += withdrawal_amount*refined_data['Annual Inflation'][i]
        portfolio -= withdrawal_amount
        equity_portion = pct_equity*portfolio    #rebalance asset allocation each year
        bond_portion = (1-pct_equity)*portfolio
    return portfolio

def prob_rand_success(num_years, wr):
    success = 0
    for i in range(0,142-num_years):
        result = calculate_rand_portfolio(num_years, i, wr)
        if result > 0:
            success += 1
    return success/(142-num_years)


prob_rand_30 = []
prob_rand_60 = []
for i in range(100):
    prob_rand_30.append(prob_rand_success(30, 0.04))
    prob_rand_60.append(prob_rand_success(60, 0.04))

fig = go.Figure()
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
                width=3)))
fig.update_layout(
    showlegend=False,
    annotations=[
        go.layout.Annotation(
            x=100,
            y=mean(prob_rand_30),
            xref="x",
            yref="y",
            text=round(mean(prob_rand_30),2),
            showarrow=True,
            arrowhead=7,
            ax=0,
            ay=-40
        ),
        go.layout.Annotation(
            x=100,
            y=mean(prob_rand_60),
            xref="x",
            yref="y",
            text=round(mean(prob_rand_60),2),
            showarrow=True,
            arrowhead=7,
            ax=0,
            ay=-40
        )
    ]
)

fig.update_layout(title='Probability of Success Based on Random Returns at 4% Withdrawal',
                   xaxis_title='Sample Iteration',
                   yaxis_title='Probability of Portfolio Success')

fig.show()
#fig.write_image('portfolio_success_random_4pct.png')



prob_rand_30_3 = []
prob_rand_60_3 = []
for i in range(100):
    prob_rand_30_3.append(prob_rand_success(30, 0.03))
    prob_rand_60_3.append(prob_rand_success(60, 0.03))

fig = go.Figure()
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
fig.update_layout(
    showlegend=False,
    annotations=[
        go.layout.Annotation(
            x=100,
            y=mean(prob_rand_30_3),
            xref="x",
            yref="y",
            text=round(mean(prob_rand_30_3),2),
            showarrow=True,
            arrowhead=7,
            ax=0,
            ay=-40
        ),
        go.layout.Annotation(
            x=100,
            y=mean(prob_rand_60_3),
            xref="x",
            yref="y",
            text=round(mean(prob_rand_60_3),2),
            showarrow=True,
            arrowhead=7,
            ax=0,
            ay=-40
        )
    ]
)
fig.update_layout(title='Probability of Success Based on Random Returns at 3% Withdrawal',
                   xaxis_title='Sample Iteration',
                   yaxis_title='Probability of Portfolio Success')
fig.show()
#fig.write_image('portfolio_success_random_3pct.png')