import stock_history

days_per_year = 365.2425
trading_days_per_year = 252
years = 10
days = int(days_per_year * years)
risk_free_rate = .015

def daily_change(prices):
    """calculates the percentage change in closing price between two consecutive trading days

    Parameters
    ----------
    prices : list
        list of closing prices

    Returns
    -------
    list
        list containing percentage changes in closing price
    """
    length = len(prices)
    changes = []
    for dayidx in range(length - 1):
        delta = (prices[dayidx + 1] - prices[dayidx]) / prices[dayidx]
        changes.append(delta)
    return changes

def stdev(inp_data):
    """calculates the population standard deviation

    Parameters
    ----------
    inp_data : list
        input data

    Returns
    -------
    float
        population standard deviation
    """
    mu = sum(inp_data) / len(inp_data)
    res = 0
    for x in inp_data:
        res += (x - mu) ** 2
    res /= len(inp_data)
    res = res ** .5
    return res

def annual_stdev(prices):
    """calculates the annual standard deviation

    Parameters
    ----------
    prices : list
        closing prices of a given stock

    Returns
    -------
    float
        annualized standard deviation of that stock
    """
    price_changes = daily_change(prices)
    std = stdev(price_changes) * (trading_days_per_year ** .5)
    return std

#net return over the given amount of years
annual_return = lambda closes: ((closes[-1] / closes[0]) ** (1 / years)) - 1

#sharpe ratio of the given stock based on closing price
sharpe = lambda prices: (annual_return(prices) - risk_free_rate) / annual_stdev(prices)

############
# spy = stock_history.price_history(["SPY"], days) #number of days in past 10 years
# spy = spy[0]
# spy_closes = spy["Adj Close"].tolist()
# print(sharpe(spy_closes))