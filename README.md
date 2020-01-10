# double-retirement

## Introduction

Traditionally, retirement planning has focused on building a portfolio that will sustain a 30-year retirement (e.g. retire at age 65 with enough funds to last until age 95). Studies have been conducted using 20th century investment returns to determine a safe withdrawal rate (SWR). The SWR would have a high probability of portfolio success (defined as not fully depleting portfolio funds within 30 years). Various studies have examined the effects of asset type, asset allocation and withdrawal rate on portfolio success over a 30-year period. 

As people live longer and try to retire earlier, it would be helpful to examine retirement planning over a longer time horizon. A growing number of people live past the age of 100, and a movement focused on retiring early has gained momentum in recent years. Under such circumstances, what is the probability of a retirement portfolio lasting 60 years instead of 30 years at a 4% withdrawal rate? Would a lower withdrawal rate increase the probability of success significantly?

### Assumptions:
1. Brokerage fees and taxes are not considered (i.e. they should be paid from withdrawn funds).
2. Inflation is based on changes in CPI.
3. Asset allocation of 50/50 is maintained year to year.
4. A single withdrawal is made on Jan. 1 each year to cover expenses for the year ahead. Yearly gains/losses on the remaining balance are calculated on Dec. 31 that year.

## Observations

The ending portfolio balance displays more volatility over a longer time horizon.

Based on historical data, length of retirement has little effect on the probability of success for withdrawal rates up to 2.5%. Rates greater than 2.5% have declining probability of success as length of retirement increases.

Randomized market returns appear to support a 95% probability of success for a 4% withdrawal rate over a 30-year period. The same randomized data would suggest that 4% over a 60-year period has a probability of success closer to 87%. The probabilities increase for the randomized data to 98% and 93%, respectively, when the withdrawal rate is decreased to 3%.

![Line Plot comparing probabilities](images/portfolio_success_4pct.png)

## Conclusion

The most risk-averse person would be advised to use a 2.5% withdrawal rate for the asset allocations analyzed here. To achieve a probability of success close to the 4% rule, a 60-year time horizon would require a withdrawal rate closer to 3%.

