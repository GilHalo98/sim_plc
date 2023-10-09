from ...temporizador import Temporizador
from ..piezas.pieza import Pieza
from ..lineas.linea import Linea
from .zona import Zona
from .tipos import TIPO_ZONA
from .eventos import EVENTOS


class Brazo_Robotico(Zona):
    def __init__(
        self,
        id: str,
        evaluacion,
        frames_movimiento: int = 20,
        frames_proceso: int = 100,
        posicion: tuple = None
    ) -> None:
        # Inicializamos la clase padre.
        super().__init__(
            id,
            TIPO_ZONA.BRAZO_ROBOTICO,
            frames_movimiento,
            posicion=posicion
        )

        # Evaluacion de la pieza para el filtro del brazo robotico.
        self.__evaluacion = evaluacion

        # ID de la zona por la que se esta esperando un evento y el evento en cuestion.
        self.__evento_esperado: tuple = None

    def __str__(self) -> str:
        msj = ''

        if self.en_espera_de_evento():
            msj += '{} en {} en espera por {} de evento {}'
            return msj.format(
                self.tipo_zona,
                self.id,
                *self.__evento_esperado
            )
    
        msj += '{} en {} en movimiento {}: {}'
        return msj.format(
            self.tipo_zona,
            self.id,
            self.temporizador_movimiento.conteo,
            self.pieza_en_zona,
        )

    @property
    def id_zona_espera(self) -> str:
        return self.__evento_esperado

    def iniciar_espera_por_evento(self, id_zona_espera: str, evento: EVENTOS) -> None:
        self.__evento_esperado = (id_zona_espera, evento)

    def terminar_espera_por_evento(self) -> None:
        self.__evento_esperado = None

    def evaluar_pieza(self, iniciar_esperas: bool = False) -> int:
        return self.__evaluacion(self, self.pieza_en_zona, iniciar_esperas)

    def en_espera_de_evento(self) -> bool:
        return True if self.__evento_esperado is not None else False

    def procesar_eventos(self, eventos_emitidos: list) -> None:
        # Verificamos que este en espera de un evento.
        if self.en_espera_de_evento():
            # Verificamos que la zona en cuestion haya emitido un evento.
            if self.__evento_esperado[0] in eventos_emitidos:
                # Si el evento fue emitido.
                if self.__evento_esperado[1] is eventos_emitidos[self.__evento_esperado[0]]:
                    # Removemos el evento de la cola de eventos.
                    eventos_emitidos.pop(self.__evento_esperado[0])
                    # Terminamos la espera por el evento.
                    self.terminar_espera_por_evento()

    def update(self, linea: Linea) -> EVENTOS:
        pass

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