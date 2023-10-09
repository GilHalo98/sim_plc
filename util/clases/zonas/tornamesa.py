from .zona import Zona
from ..lineas.linea import Linea
from .tipos import TIPO_ZONA
from .eventos import EVENTOS


class Tornamesa(Zona):
    def __init__(
        self,
        id: str,
        evaluacion,
        frames_movimiento: int = 20,
        posicion: tuple = None
    ) -> None:
        # Inicializamos la clase padre.
        super().__init__(
            id,
            TIPO_ZONA.TORNAMESA,
            frames_movimiento,
            posicion=posicion
        )

        self.__evaluacion = evaluacion

    def evaluar_pieza(self, iniciar_esperas: bool = False) -> int:
        return self.__evaluacion(self, self.pieza_en_zona, iniciar_esperas)

    def step(self, linea: Linea) -> EVENTOS:
        # Esperamos a que termine el temporizador para el movimiento.
        if not self.temporizador_movimiento.en_espera():
            # Si la zona no es final en la linea.
            if not linea.elemento_es_hoja(self.id):
                # Recuperamos la zona siguiente.
                zona_siguiente: Zona = linea.elementos[
                    linea.expandir(self.id)[self.evaluar_pieza(True)]
                ]

                # Si la zona siguiente esta libre.
                if zona_siguiente.zona_libre():
                    # Movemos la pieza.
                    zona_siguiente.ingresar_pieza(self.mover_pieza())

            # Reseteamos el temporizador del movimiento.
            self.temporizador_movimiento.reset()

        # Si la zona no esta libre.
        if not self.zona_libre():
            # Si la zona no es final en la linea.
            if not linea.elemento_es_hoja(self.id):
                # Recuperamos la zona siguiente.
                zona_siguiente: Zona = linea.elementos[
                    linea.expandir(self.id)[self.evaluar_pieza()]
                ]

                # Si la zona siguiente esta libre.
                if zona_siguiente.zona_libre():
                    # Continuamos con el conteo del temprizador de movimiento.
                    self.temporizador_movimiento.update()