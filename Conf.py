class Conf():
    _instance = None
    _initialized = False

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @staticmethod
    def initialize(openfireServer,openfirePassword):
        if not Conf._initialized:
            Conf._instance = Conf()
            Conf._instance.openfireServer = openfireServer
            Conf._instance.openfirePassword = openfirePassword
            Conf._initialized = True
    
    def get_openfire_server(self):
        return self.openfireServer
    
    def get_openfire_password(self):
        return self.openfirePassword