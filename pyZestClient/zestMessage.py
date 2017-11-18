__author__ = 'pooyadav'

"""
A zest message consists of
Header
Token(Optional)
Options
Payload
"""


class ZestMessage():
    def __init__(self, zest_header, token, payload):
        """

        :param zest_header:
        :param token:
        :param payload:
        """
        self.zest_header = zest_header
        self.payload = payload
        self.token = token

    @property
    def create_token(self):
        return self.token, len(self.token) * 8

    def create_options(self):
        pass

    def create_get_options(self):
        pass

    def create_option(self):
        pass

    def create_post_options(self):
        pass
