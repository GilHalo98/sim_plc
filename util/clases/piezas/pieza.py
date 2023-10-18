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

        # Status de las pruebas.
        self.__status: dict = dict()

        # Tipo de pieza.
        self.__tipo_pieza: TIPO_PIEZA = TIPO_PIEZA.INDEFINIDA

    def __str__(self) -> str:
        msj: str = 'ID: {}'
        msj += '\tTipo de pieza: {}'
        msj += '\tDatamatrix: {}'
        msj += '\tStatus inspeccion: {}'

        return msj.format(
            self.__id,
            self.__tipo_pieza,
            self.__data_matrix,
            self.__status
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
    def tipo_pieza(self) -> TIPO_PIEZA:
        return self.__tipo_pieza

    @data_matrix.setter
    def data_matrix(self, data_matrix: str) -> None:
        self.__data_matrix = data_matrix

    @tipo_pieza.setter
    def tipo_pieza(self, tipo_pieza: TIPO_PIEZA) -> None:
        self.__tipo_pieza = tipo_pieza

    def set_status(self, **new_status) -> None:
        for id_status in new_status:
            self.__status[id_status] = new_status[id_status]