from external_ingestor.utils.dynamics import __getclass__
from external_ingestor.utils.logging import get_logger


class ExternalIngestor(object):

    def __init__(self, domain, transformer, sink, client, method, client_settings=None, sink_settings=None):
        self.name = self.__class__.__name__
        self.logger = get_logger(self.name)
        self.method = method
        self.domain = domain
        self.transformer_name = transformer
        self.client = __getclass__("client", client)(self.domain, client_settings)
        self.logger.info("Client object loaded {}".format(self.client))
        self.sink = __getclass__("sink", sink)(sink_settings)
        self.logger.info("Sink object loaded {}".format(self.sink))

    def run(self,target_path, start_time, end_time=None):
        payload = getattr(self.client, self.method)(target_path, start_time, end_time)
        self.transformer = __getclass__("transformers", self.transformer_name)(payload)
        self.logger.info("Transformation object loaded {}".format(self.transformer))
        self.transformer.transform()
        self.sink.sink(self.transformer.dataframe)


