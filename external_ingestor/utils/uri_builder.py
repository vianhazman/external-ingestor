class UriBuilder(object):
    def __init__(self, domain):
        self.domain = domain

    def get_full_path(self, path=None, parameters=None):
        api_path = "%(domain)s%(path)s" % {
                'domain': self.domain,
                'path': path
        }

        if parameters:
            filters = ""
            for key, value in parameters.items():
                filters += "%(key)s=%(value)s&" % {
                    'key': key,
                    'value': value
                }
            api_path = "%(domain)s%(path)s?%(filters)s" % {
                'domain': self.domain,
                'path': path,
                'filters': filters[:-1]
            }

        return api_path