from unittest import TestCase

from mock import patch

import external_ingestor
from external_ingestor.ExternalIngestor import ExternalIngestor
from external_ingestor.client import ZendeskClient
from external_ingestor.sink import PostgresSink
from external_ingestor.transformers import ZendeskTransformer


class RunnerTest(TestCase):
    def setUp(self):
        domain = "https://vianhazman.zendesk.com"
        sink = "PostgresSink"
        client = "ZendeskClient"
        transformer = "ZendeskTransformer"
        method = "get_ticket_incremental"
        client_settings = {
            "email" : "vianhazman@gmail.com",
            "password" : "oHdTQvrQwqXDOLaZohRS9pyK19vMdQOYYIYwA3bR"
        }
        sink_settings = {
            "user": "postgres",
            "pass": "postgres",
            "port": 5432,
            "db": "postgres",
            "host": "localhost",
            "table_name": "test_table_3"
        }
        self.target_path = "/api/v2/incremental/tickets.json"
        self.runner = ExternalIngestor(domain, transformer, sink, client, method, client_settings, sink_settings)

    @patch.object(ExternalIngestor, 'run')
    def test_run(self, mock_request):
        epoch_time = 1591013586
        self.runner.run(self.target_path, epoch_time)
        mock_request.assert_called_once_with(self.target_path, epoch_time)

