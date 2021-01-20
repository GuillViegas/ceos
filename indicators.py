import pandas as pd


def ema(dataset, field, span=10):
    """ Exponential Moving Average """
    return dataset[field].ewm(span=span, adjust=False).mean()


def rsi(dataset, begin_date, end_date, field, span=14):
    """ Relative Strength Index """
    dataset = pd.concat([dataset.loc[:begin_date].tail(span), dataset.loc[begin_date:end_date]])

    delta = dataset[field].diff()
    
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0 

    gain_avg = up.rolling(window=span).mean()
    loss_avg = down.abs().rolling(window=span).mean()

    rsi = 100 - (100/ (1 + (gain_avg/loss_avg)))

    return  rsi[span:]

def bb(dataset, begin_date, end_date, field, span=20, multi_factor=2):
    """ Bollinger Bands """
    dataset = pd.concat([dataset.loc[:begin_date].tail(span), dataset.loc[begin_date:end_date]])

    sma = dataset[field].rolling(window=span).mean()
    factor = multi_factor * dataset[field].rolling(window=span).std()
    
    down_bb = sma - factor
    up_bb = sma + factor

    return sma[span:], down_bb[span:], up_bb[span:]

