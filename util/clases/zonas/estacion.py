import random

from ...temporizador import Temporizador
from ..lineas.linea import Linea
from .zona import Zona
from .tipos import TIPO_ZONA
from ..piezas.status import STATUS
from ..zonas.eventos import EVENTOS


class Estacion(Zona):
    def __init__(
        self,
        id: str,
        procesar_pieza,
        frames_movimiento: int = 20,
        frames_proceso: int = 200,
        posicion: tuple = None
    ) -> None:
        # Inicializamos la clase padre.
        super().__init__(
            id,
            TIPO_ZONA.ESTACION,
            frames_movimiento,
            posicion=posicion,
            descripcion='Estación de operaciones'
        )

        # Id de la pieza anteriormente inspeccionada.
        self.__id_pieza_inspeccionada: int = None

        # Funcion de procesamiento de pieza.
        self.__procesar_pieza = procesar_pieza

        # Temporizador de espera para terminar el proceso.
        self.__temporizador_proceso: Temporizador = Temporizador(frames_proceso)

    def __str__(self) -> str:
        msj = '{} en {} en {} {}: {}'
        return msj.format(
            self.tipo_zona,
            self.id,
            'Movimiento' if self.proceso_terminado() else 'Proceso',
            '{}'.format(
                self.temporizador_movimiento.conteo if self.proceso_terminado() else self.__temporizador_proceso.conteo
            ),
            self.pieza_en_zona,
        )

    def proceso_terminado(self) -> bool:
        return not self.__temporizador_proceso.en_espera()

    def update(self, linea: Linea) -> EVENTOS:
        evento = None
        if not self.zona_libre():
            self.__temporizador_proceso.update()

            if self.proceso_terminado():
                evento = self.__procesar_pieza(self, self.pieza_en_zona)

        return evento

    def step(self, linea: Linea) -> EVENTOS:
        evento = None
        if self.proceso_terminado():
            if not self.zona_libre():
                if not linea.elemento_es_hoja(self.id):
                    zona_siguiente: Zona = linea.elementos[linea.expandir(self.id)[0]]

                    if zona_siguiente.zona_libre():
                        self.temporizador_movimiento.update()
            else:
                self.temporizador_movimiento.reset()
                self.__temporizador_proceso.reset()

        else:
            evento = self.update(linea)

        if not self.temporizador_movimiento.en_espera():
            if not linea.elemento_es_hoja(self.id):
                zona_siguiente: Zona = linea.elementos[linea.expandir(self.id)[0]]

                if zona_siguiente.zona_libre():
                    zona_siguiente.ingresar_pieza(self.mover_pieza())

        return evento
            