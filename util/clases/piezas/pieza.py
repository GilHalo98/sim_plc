from .status import STATUS
from .tipos import TIPO_PIEZA

class Pieza():
    def __init__(
        self,
        id: int
    ) -> None:
        # ID de la pieza.
        self.__id: int = id

        # Datamatrix de la pieza.
        self.__data_matrix: str = None

        # Status de la piezaz.
        self.__status: STATUS = STATUS.INDEFINIDA

        # Status de la prueba de leak.
        self.__status_leak: STATUS = STATUS.INDEFINIDA

        # Tipo de pieza.
        self.__tipo_pieza: TIPO_PIEZA = TIPO_PIEZA.INDEFINIDA

    def __str__(self) -> str:
        mjs: str = 'ID: {}\tTipo de pieza: {}\tDatamatrix: {}\tStatus inspeccion: {}\tStatus leak: {}'

        return mjs.format(
            self.__id,
            self.__tipo_pieza,
            self.__data_matrix,
            self.__status,
            self.__status_leak
        )

    @property
    def id(self) -> int:
        return self.__id

    @property
    def data_matrix(self) -> str:
        return self.__data_matrix

    @property
    def status(self) -> STATUS:
        return self.__status

    @property
    def status_leak(self) -> STATUS:
        return self.__status_leak

    @property
    def tipo_pieza(self) -> TIPO_PIEZA:
        return self.__tipo_pieza

    @data_matrix.setter
    def data_matrix(self, data_matrix: str) -> None:
        self.__data_matrix = data_matrix

    @status.setter
    def status(self, status: STATUS) -> None:
        self.__status = status

    @status_leak.setter
    def status_leak(self, status_leak: STATUS) -> None:
        self.__status_leak = status_leak

    @tipo_pieza.setter
    def tipo_pieza(self, tipo_pieza: TIPO_PIEZA) -> None:
        self.__tipo_pieza = tipo_pieza