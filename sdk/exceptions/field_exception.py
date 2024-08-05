class FieldException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class InvalidFieldException(FieldException):
    pass


class MissingFieldException(FieldException):
    def __init__(self, message, is_cred: bool = False):
        if is_cred:
            self.message = (f"Mandatory credentials are missing. "
                            f"Please ensure you provide: {message}")
        else:
            self.message = f"Missing {message}"
        super().__init__(self.message)
