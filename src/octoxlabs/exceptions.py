class ApiException(Exception):
    pass


class NoDiscoveryError(Exception):
    pass


class NotFound(Exception):
    pass


class CantCreate(Exception):
    pass


class CantUpdate(Exception):
    pass


class CantDelete(Exception):
    pass
