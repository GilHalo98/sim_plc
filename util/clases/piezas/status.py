import enum

class STATUS(enum.Enum):
    INDEFINIDA = enum.auto()
    OK = enum.auto()
    RECHAZADA = enum.auto()
    NO_DATA_MATRIX = enum.auto()