import time

from external_ingestor.client.RestApiClient import RestApiClient


class ZendeskClient(RestApiClient):
    def __init__(self, domain, settings):
        authentication = "{}/token".format(settings['email']), settings['password']
        super(ZendeskClient, self).__init__(domain, authentication)

    def get_ticket_incremental(self, path, dstart, *args):
        args = {"start_time": dstart}
        ticket_batch = []
        while True:
            result, response = self.__get__(path, args)
            if response.status_code == 429:
                delay = int(response.headers['retry-after'])
                time.sleep(delay)
            ticket_batch.extend(result['tickets'])

            if args['start_time'] == result['end_time']:
                break
            args['start_time'] = result['end_time']
        return ticket_batch
