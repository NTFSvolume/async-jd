from pyjd.endpoints import Action
from pyjd.jd_types import APIQuery


class Polling(Action, endpoint="polling"):
    def poll(self, query_params=APIQuery.default()):
        """Poll for APIQuery."""

        params = [query_params.__json__()]
        return self.action("/poll", params)
