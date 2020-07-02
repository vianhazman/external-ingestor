import logging

import requests

from external_ingestor.utils.json_tools import json_to_dict
from external_ingestor.utils.logging import get_logger
from external_ingestor.utils.uri_builder import UriBuilder


class RestApiClient:

    def __init__(self, target_domain, authentication=None, header=None, max_retry=2):
        self.name = self.__class__.__name__
        self.logger = get_logger(self.name)
        self.logger.setLevel(logging.INFO)
        self.target_domain = target_domain
        self.header = header
        self.max_retry = max_retry
        self.uri_builder = UriBuilder(target_domain, )
        self.session = requests.Session()
        self.session.auth = authentication

    def get_class_name(self):
        return self.name

    def get_target_domain(self):
        return self.target_domain

    def get_auth(self):
        return self.session.auth

    def get_header(self):
        if self.header:
            header = dict(self.header)
            # Make sure parsed as JSON
            header['content-type'] = 'application/json'
            header['accept'] = 'application/json'
            return header
        return None

    def get_max_retry(self):
        return self.max_retry

    def generate_endpoint(self, path, args=None):
        args = args if args else {}
        uri = self.uri_builder.get_full_path(path, args)
        return uri

    def __get__(self, path, args=None, attempt=1):
        uri = self.generate_endpoint(path, args)
        self.logger.info("GET {}".format(uri))
        try:
            request = self.session.get(uri, headers=self.get_header())
            result = json_to_dict(request.content)

            if request.status_code == 200:
                return result, request

            else:
                self.logger.error(f'{self.get_class_name()} failed to GET ({uri}): | attempt: {attempt} | \
                 HTTP code:{request.status_code}  / err msg: {result}')

                if self.get_max_retry() == attempt:
                    return result, request
                else:
                    self.get(self, path, args, attempt + 1)

        except Exception as e:
            self.logger.error(str(e))
            return None, 500
