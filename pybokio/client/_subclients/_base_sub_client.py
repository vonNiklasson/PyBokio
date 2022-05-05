class BaseSubClient:
    def __init__(self, client, **kwargs):
        """

        :type base: pybokio.BokioClient
        """
        self.__client = client

    @property
    def client(self):
        """

        :rtype: pybokio.BokioClient
        """
        return self.__client
