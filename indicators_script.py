'''
Script to ...
:author: Guilherme Viegas de Faria <guivfaria@gmail.com>
'''

import argparse
from datetime import datetime
import os

from assets import AssetTimeSeries
import indicators

def parser_arguments():
    """ Read arguments from command line. """

    parser = argparse.ArgumentParser(description='Calculates some indicators from bitcoin historical data')
    
    parser.add_argument('-file', type=str, help="Provide the path to bitcoin historical data.", required=True)
    parser.add_argument('-begin_date', type=str, help="The beginning of the time series in the following format 'YYYY-MM-DD HH:MM:SS'.", required=True)
    parser.add_argument('-end_date', type=str, help="The end of the time series in the following format 'YYYY-MM-DD HH:MM:SS'.", required=True)

    args = parser.parse_args()
    
    return args


def main():
    asset = AssetTimeSeries(path=args.file)

    ema = asset.result_set(indicators.ema, args.begin_date, args.end_date)
    rsi = asset.result_set(indicators.rsi, args.begin_date, args.end_date)
    sma, down_band, up_band = asset.result_set(indicators.bollinger_bands, args.begin_date, args.end_date)

    df = rsi.to_frame(name='ema')\
        .join(rsi.to_frame(name='rsi'))\
        .join(sma.to_frame(name='sma'))\
        .join(down_band.to_frame(name='down_band'))\
        .join(up_band.to_frame(name='up_band'))

    df.to_csv('indicators.csv', index=True)


if __name__ == "__main__":
    args = parser_arguments()
    main()