from datetime import datetime
import inspect
import pandas as pd


class BitcoinTimeSeries:

    def __init__(self, dataset=None, path=None):
        if not (dataset or path):
            raise ValueError("BitcoinTimeSeries needs to be inicialized with some dataset")
        
        self.dataset = dataset or pd.read_csv(path)
        self.dataset['Close'].fillna(method='ffill', inplace=True)

        self.date_from_timestamp()

    def date_from_timestamp(self):
        if not 'Timestamp' in self.dataset:
            raise ValueError("Dataset has no timestamp field")

        dates = self.dataset['Timestamp'].apply(datetime.fromtimestamp)
        
        self.dataset['Date'] = dates
        self.dataset.set_index('Date', inplace=True)

        return dates

    def result_set(self, begin_date, end_date, field, indicator, **kwargs):
        if 'begin_date' in inspect.getargspec(indicator).args:
            return indicator(self.dataset, begin_date, end_date, field, **kwargs)

        return indicator(self.dataset.loc[begin_date:end_date], field, **kwargs)