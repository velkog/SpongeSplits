class FormatterException(Exception):
    def __init__(self, error_template, **kwargs):
        error = error_template.format_map(kwargs)
        super(FormatterException, self).__init__(error)


class InvalidOptionException(FormatterException):
    ERROR_TEMPLATE: str = "Error: invalid option '{option}' selected."

    def __init__(self, option: str):
        super(InvalidOptionException, self).__init__(self.ERROR_TEMPLATE,
                                                     option=option)


class OutOfRangeOptionException(FormatterException):
    ERROR_TEMPLATE: str = "Error: option '{option}' is out of range."

    def __init__(self, option: str):
        super(OutOfRangeOptionException, self).__init__(self.ERROR_TEMPLATE,
                                                        option=option)
