import datetime
import pandas as pd
import pytz

from external_ingestor.transformers.BaseTransformer import BaseTransformer


class ZendeskTransformer(BaseTransformer):

    def __init__(self, payload):
        super(ZendeskTransformer, self).__init__(payload)

    def transform(self):
        self.transform_dict()
        self.load_to_df()
        str_time_to_utc_column = ["created_at", "updated_at"]
        for i in str_time_to_utc_column:
            self.dataframe[i] = pd.to_datetime(self.dataframe[i], utc=True)

        self.dataframe['generated_timestamp'] = self.dataframe['generated_timestamp'] = pd.to_datetime(self.dataframe[i], utc=True)

        return self.dataframe
