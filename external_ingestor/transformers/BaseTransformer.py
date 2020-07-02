import pandas as pd
from external_ingestor.utils.json_tools import flatten_dict
from datetime import datetime
import pytz

from external_ingestor.utils.logging import get_logger


class BaseTransformer:

    def __init__(self, payload):
        """
        Base Transformation Class.
        Contains basic transformation methods for response.
        """
        self.name = self.__class__.__name__
        self.logger = get_logger(self.name)
        self.payload = payload
        self.dataframe = None


    def transform_dict(self):
        """
        Standard dict transformation to be loaded into Pandas Dataframe
        :return: dict
        """
        payload = self.payload
        self.payload = map(flatten_dict, payload)
        self.logger.info("Payload transformed")
        return self.payload

    def load_to_df(self):
        """
        Load dict object to class Pandas Dataframe
        :param normalize_columns: Boolean
        :return: Pandas Dataframe
        """
        df = pd.DataFrame.from_dict(self.payload)
        df['load_time'] = pd.to_datetime(datetime.now(), utc=True)
        self.dataframe = df
        self.logger.info("Payload loaded into dataframe")
        return self.dataframe


