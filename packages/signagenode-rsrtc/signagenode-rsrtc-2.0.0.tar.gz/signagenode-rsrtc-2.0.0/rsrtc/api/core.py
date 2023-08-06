
from twisted.internet.defer import succeed

from ebs.linuxnode.modapi.engine import ModularHttpApiEngine


class RsrtcApiCoreEngine(ModularHttpApiEngine):
    _prefix = "rsrtc"
    _api_probe = 'api_test_connection'
    _api_tasks = []
    _api_reconnect_frequency = 30
    _api_baseurl = 'config:rsrtc_api_url'
    _api_headers = {'Content-Type': 'application/json'}

    _api_ep_test_connection = 'bus-schedules'

    @property
    def api_token(self):
        return succeed(None)

    def api_token_reset(self):
        return succeed(None)

    def _api_basic_params(self, token):
        return {'_query': []}

    def _api_test_query_params(self, token):
        rv = self._api_basic_params(token)
        rv['_query'].append(('code', 'KTH'))
        return rv

    def _api_ep_test_connection_handler(self, response):
        return succeed(True)

    def api_test_connection(self):
        return self._api_execute(
            self._api_ep_test_connection,
            self._api_test_query_params,
            self._api_ep_test_connection_handler
        )
