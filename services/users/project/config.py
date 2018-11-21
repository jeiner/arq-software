

class BaseConfig:
    """ configuracion base"""
    TESTING = False


class DevelopmentConfig(BaseConfig):
    """configuracion del desarrollo """
    pass


class TestingConfig(BaseConfig):
    """configuracion de prueba """
    pass


class TEstingConfig(BaseConfig):
    """configuracion de prueba """
    TESTING = True


class ProductionConfig(BaseConfig):
    """configuracion de produccion """
    pass
