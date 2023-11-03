import enum

class TIPO_REPORTE(enum.Enum):
    INDEFINIDO = enum.auto()
    INSPECCION_FINAL_OK = enum.auto()
    INSPECCION_FINAL_RECHAZO = enum.auto()
    INSPECCION_LEAK_OK = enum.auto()
    INSPECCION_LEAK_RECHAZO = enum.auto()
    NO_DATA_MATRIX_DETECTADA = enum.auto()
    DATA_MATRX_GRABADO = enum.auto()