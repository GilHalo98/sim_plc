from ...db_manager import Dbm
from ...temporizador import Temporizador

class Plc():

    def __init__(
        self,
        id: str,
        database_manager: Dbm
    ) -> None:
        # ID de la instancia.
        self.__id: str = id

        # Cola de actualización, indica como realizara
        # las actualizaciones de las zonas.
        self.__cola_actualizacion: list[str] = list()

        # Cola de eventos del grafo.
        self.__cola_eventos: dict  = dict()

        # Temporizador de consultas a DB.
        self.__temporizador_db: Temporizador = Temporizador(20)

        # Instancia del database manager.
        self.__database_manager: Dbm = database_manager

    def __str__(self) -> None:
        pass

    @property
    def cola_eventos(self) -> dict:
        return self.__cola_eventos

    def procesar_percepcion(self, linea: 'Linea') -> dict:
        percepcion: dict = dict()
        for id_zona in linea.elementos:
            zona: 'Zona' = linea.elementos[id_zona]

            if not zona.zona_libre():
                pieza: 'Pieza' = zona.pieza_en_zona

                if pieza.data_matrix != None:
                    percepcion[zona.id] = pieza

        return percepcion

    def generar_cola_actualizacion(self, linea: 'Linea') -> None:
        # Realiza un recorrido DFS para generar
        # la cola de actualizacion.
        # Primero se limpia la cola de actualizacion.
        self.__cola_actualizacion: list[str] = list()

        # Realizamos un recorrido DFS del grafo.
        self.__cola_actualizacion.append(
            linea.DFS(linea.zona_inicial, self.__cola_actualizacion)
        )

    def update(self, linea: 'Linea') -> None:
        zonas_actualizadas: list = list()
        
        if not self.__temporizador_db.en_espera():
            self.__database_manager.update_estado_piezas(
                linea.id,
                self.procesar_percepcion(linea)
            )
            self.__temporizador_db.reset()
        self.__temporizador_db.update()

        for id_zona in self.__cola_actualizacion:
            if id_zona not in zonas_actualizadas:
                zonas_actualizadas.append(id_zona)
                zona = linea.elementos[id_zona]
                evento_emitido = zona.step(linea)

                if evento_emitido is not None:
                    emisor, evento = evento_emitido
                    self.__cola_eventos[emisor] = evento

        for id_zona in linea.elementos:
            zona = linea.elementos[id_zona]
            zona.procesar_eventos(self.__cola_eventos)
