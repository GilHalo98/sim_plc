import enum


class TIPO_ZONA(enum.Enum):
    CONVEYOR = enum.auto()
    ESTACION = enum.auto()
    TORNAMESA = enum.auto()
    BRAZO_ROBOTICO = enum.auto()