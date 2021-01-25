from datetime import datetime
import pandas as pd


class AssetTimeSeries:

    def __init__(self, dataset=None, path=None, data_based_index=False):
        if not (dataset or path):
            raise ValueError("AssetTimeSeries needs to be inicialized with some dataset")
        
        self.dataset = dataset or pd.read_csv(path)
        self.dataset['Close'].fillna(method='ffill', inplace=True)

        if data_based_index:
            self.date_idx_from_timestamp()

        else:
            self.dataset.set_index('Timestamp', inplace=True)


    def date_idx_from_timestamp(self):
        """ Create a date-based index from Timestamp field. """

        if not 'Timestamp' in self.dataset:
            raise ValueError("Dataset has no Timestamp field")

        dates = self.dataset['Timestamp'].apply(datetime.fromtimestamp)
        
        self.dataset['Date'] = dates
        self.dataset.set_index('Date', inplace=True)

        return dates

    def result_set(self, indicator, begin_date, end_date, field='Close', **kwargs):
        """ Calculates a given indicator from the dataset. Indicators are available at indicators.py. """

        begin_date = datetime.strptime(begin_date, "%Y-%m-%d %H:%M:%S")
        end_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
    
        begin = datetime.timestamp(begin_date)
        end = datetime.timestamp(end_date)

        return indicator(self.dataset, begin, end, field)