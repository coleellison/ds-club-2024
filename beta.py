import stock_history

days_per_year = 365.2425
trading_days_per_year = 252
years = 10
days = int(days_per_year * years)
risk_free_rate = .015

spy = stock_history.price_history(["SPY"], days) #number of days in past 10 years
spy = spy[0]
spy_closes = spy["Adj Close"].tolist() #hard encoded for the sake of our market average.

def daily_change(prices): #borrowed from sharpe_ratio
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

def covariance(stock_closes, market_closes = spy_closes):
    """calculates the covariance of our given stock against the market

    Parameters
    ----------
    stock_closes : list
        adjusted close prices of the given stock
    market_closes : list, optional
        adjusted close prices of the market index, by default spy_closes

    Returns
    -------
    float
        covariance of the stock against the market
    """
    stock_hist_length = len(stock_closes)
    market_hist_length = len(market_closes)
    if stock_hist_length != market_hist_length:
        max_length = min(stock_hist_length, market_hist_length)
        stock_closes = stock_closes[-1 * max_length:]
        market_closes = market_closes[-1 * max_length:]
    stock_changes = daily_change(stock_closes)
    market_changes = daily_change(market_closes)
    length = len(stock_changes)
    avg_stock_change = sum(stock_changes) / length
    avg_market_change = sum(market_changes) / length
    cov = 0
    for i in range(length):
        stock_delta = stock_changes[i] - avg_stock_change
        market_delta = market_changes[i] - avg_market_change
        cov += (stock_delta * market_delta) / (length - 1)
    return cov

def variance(stock_closes):
    """calculates the variance of the given stock

    Parameters
    ----------
    stock_closes : list
        adjusted close prices of the stock

    Returns
    -------
    float
        variance in daily price changes of the stock
    """
    stock_changes = daily_change(stock_closes)
    length = len(stock_changes)
    avg_stock_change = sum(stock_changes) / length
    var = 0
    for i in range(length):
        stock_delta = stock_changes[i] - avg_stock_change
        var += (stock_delta ** 2) / (length - 1)
    return var

def beta(stock_closes, market_closes = spy_closes):
    """calculates the beta of a given stock against the market

    Parameters
    ----------
    stock_closes : list
        adjusted closing prices of the given stock
    market_closes : list, optional
        adjusted close prices of the market index, by default spy_closes

    Returns
    -------
    float
        beta of the stock against the market
    """
    cov = covariance(stock_closes, market_closes)
    var = variance(stock_closes)
    return cov / var

####################
# goog_closes = stock_history.price_history(["GOOG"], days)[0]["Adj Close"].tolist()
# print(beta(goog_closes, spy_closes))