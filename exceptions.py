class CalculatorError(Exception):
    pass


class InvalidDecimalInputError(CalculatorError):
    pass


class BCD2421Error(CalculatorError):
    pass


class InvalidFormatError(CalculatorError):
    pass


class ExponentOverflowError(CalculatorError):
    pass


class ExponentUnderflowError(CalculatorError):
    pass


class DivisionByZeroError(CalculatorError):
    pass
