import pandas as pd


def ema(dataset, begin, end, field, span=10):
    """ Exponential Moving Average 
        ref: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.ewm.html 
    """
    return dataset.loc[begin:end][field].ewm(span=span, adjust=False).mean()


def rsi(dataset, begin, end, field, span=14, offset=True):
    """ Relative Strength Index """
    if offset:
        dataset = pd.concat([dataset.loc[:begin].tail(span), dataset.loc[begin:end]])

    delta = dataset[field].diff()
    
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0 

    gain_avg = up.rolling(window=span).mean()
    loss_avg = down.abs().rolling(window=span).mean()

    rsi = 100 - (100/ (1 + (gain_avg/loss_avg)))

    if offset:
        rsi = rsi[span:]

    return  rsi

def bollinger_bands(dataset, begin, end, field, span=20, multi_factor=2, offset=True):
    """ Bollinger Bands """
    
    if offset:
        dataset = pd.concat([dataset.loc[:begin].tail(span), dataset.loc[begin:end]])

    sma = dataset[field].rolling(window=span).mean()
    factor = multi_factor * dataset[field].rolling(window=span).std()
    
    down_band = sma - factor
    up_band = sma + factor

    if offset:
        sma, down_band, up_band = sma[span:], down_band[span:], up_band[span:]

    return sma, down_band, up_band

