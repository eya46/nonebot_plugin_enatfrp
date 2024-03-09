class NatFrpException(Exception):
    pass


class NatFrpAPIException(NatFrpException):
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message

    def __repr__(self):
        return f"eNatFrpAPIException(status_code={self.code}, message={self.message!r})"
