from ...temporizador import Temporizador
from ..piezas.pieza import Pieza
from ..lineas.linea import Linea
from .tipos import TIPO_ZONA
from .eventos import EVENTOS

class Zona():
    def __init__(
        self,
        id: str,
        tipo_zona: TIPO_ZONA,
        frames_movimiento: int,
        conexion_con_linea: tuple = None,
        posicion: tuple = None,
        descripcion: str = ''
    ) -> None:
        # ID de la zona dentro de la linea.
        self.__id: str = id

        # Descripcion de la zona.
        self.__descripcion: str = descripcion

        # Indica el tipo de zona.
        self.__tipo_zona: TIPO_ZONA = tipo_zona

        # Pieza vinculada a la zona.
        self.__pieza_en_zona: Pieza = None

        # Temporizador de espera para terminar el movimiento.
        self.__temporizador_movimiento: Temporizador = Temporizador(
            frames_movimiento
        )

        # Conexion entre lineas.
        self.__conexion_con_linea: tuple = conexion_con_linea

        # Posición en el grid del gui de la zona.
        self.__posicion: tuple = posicion

    def __str__(self) -> str:
        msj = '{} en {} en movimiento {}: {}'
        return msj.format(
            self.__tipo_zona,
            self.__id,
            self.__temporizador_movimiento.conteo,
            self.__pieza_en_zona,
        )

    @property
    def id(self) -> str:
        return self.__id

    @property
    def descripcion(self) -> str:
        return self.__descripcion

    @property
    def tipo_zona(self) -> TIPO_ZONA:
        return self.__tipo_zona

    @property
    def pieza_en_zona(self) -> Pieza:
        return self.__pieza_en_zona

    @property
    def temporizador_movimiento(self) -> Temporizador:
        return self.__temporizador_movimiento

    @property
    def conexion_con_linea(self) -> tuple:
        return self.__conexion_con_linea

    @property
    def posicion(self) -> tuple:
        return self.__posicion

    @descripcion.setter
    def descripcion(self, descripcion: str) -> None:
        self.__descripcion = descripcion

    @conexion_con_linea.setter
    def conexion_con_linea(self, conexion: tuple) -> None:
        self.__conexion_con_linea = conexion

    def es_interconexion(self) -> bool:
        return False if self.__conexion_con_linea is None else True

    def ingresar_pieza(self, pieza: Pieza) -> bool:
        if pieza is not None:
            if self.zona_libre():
                self.__pieza_en_zona = pieza

                return True

        return False

    def mover_pieza(self) -> Pieza:
        if not self.zona_libre():
            pieza = self.__pieza_en_zona
            self.__pieza_en_zona = None
            return pieza

    def zona_libre(self) -> bool:
        return True if self.__pieza_en_zona is None else False

    def en_espera_de_evento(self) -> bool:
        return False

    def procesar_eventos(self, eventos_emitidos: list) -> None:
        # Procesa un evento pasado.
        pass

    def update(self, linea: Linea) -> EVENTOS:
        # procesa o realiza una decicion.
        pass

    def step(self, linea: Linea) -> EVENTOS:
        if not self.__temporizador_movimiento.en_espera():
            if not linea.elemento_es_hoja(self.id):
                zona_siguiente: Zona = linea.elementos[
                    linea.expandir(self.id)[0]
                ]

                if(
                    zona_siguiente.zona_libre()
                    and not zona_siguiente.en_espera_de_evento()
                ):
                    zona_siguiente.ingresar_pieza(self.mover_pieza())

            else:
                linea_siguiente: Linea = self.__conexion_con_linea[0]
                zona_siguiente: Zona = linea_siguiente.elementos[
                    self.__conexion_con_linea[1]
                ]

                if(
                    zona_siguiente.zona_libre()
                    and not zona_siguiente.en_espera_de_evento()
                ):
                    zona_siguiente.ingresar_pieza(self.mover_pieza())

            self.__temporizador_movimiento.reset()

        if not self.zona_libre():
            if not linea.elemento_es_hoja(self.id):
                zona_siguiente: Zona = linea.elementos[
                    linea.expandir(self.id)[0]
                ]
                if(
                    zona_siguiente.zona_libre()
                    and not zona_siguiente.en_espera_de_evento()
                ):
                    self.__temporizador_movimiento.update()

            else:
                if self.es_interconexion():
                    linea_siguiente: Linea = self.__conexion_con_linea[0]
                    zona_siguiente: Zona = linea_siguiente.elementos[
                        self.__conexion_con_linea[1]
                    ]

                    if(
                        zona_siguiente.zona_libre()
                        and not zona_siguiente.en_espera_de_evento()
                    ):
                        self.__temporizador_movimiento.update()