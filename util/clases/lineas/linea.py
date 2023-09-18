import requests

from ...temporizador import Temporizador
from ...estructuras.grafo import Grafo
from ..piezas.pieza import Pieza
from ..zonas.tipos import TIPO_ZONA


class Linea(Grafo):
    def __init__(
        self,
        id_linea: str,
        zona_inicial: str = None,
        zonas_finales: list = list(),
        conexiones: dict = dict(),
        zonas: dict = dict(),
        lineas_conectadas: dict = dict()
    ) -> None:
        # Inicializamos la clase padre, que este en caso es un grafo.
        super().__init__(conexiones, zonas)

        # ID de la linea.
        self.__id_linea: str = id_linea

        # Zona inicial de la linea.
        self.__zona_inicial: str = zona_inicial

        # Lista de zonas finales de la linea.
        self.__zonas_finales: list =  zonas_finales

        # Diccionario de lineas interconectadas y en que zona final.
        self.__lineas_conectadas: dict = lineas_conectadas

        # Cola de actualización de las zonas de la linea.
        self.__cola_actualizacion: list = list()

        # Diccionario de eventos emitidos por las zonas.
        self.__cola_eventos: dict = dict()

        # Temporizador para mandar un request POST al API.
        self.__temporizador_request = Temporizador(10)

        # Generamos la cola de actualización de la linea.
        self.generar_cola_actualizacion()

        # Conectamos la linea inicial con otras lineas.
        self.conectar_lineas()

    def __str__(self) -> str:
        msj = 'Linea {}:\n'
        msj += 'Eventos: {}\n'

        for id_zona in self.elementos:
            zona = self.elementos[id_zona]
            msj += str(zona) + '\n'

        return msj.format(self.__id_linea, self.__cola_eventos)

    @property
    def id(self) -> str:
        return self.__id_linea

    @property
    def zonas_finales(self) -> list:
        return self.__zonas_finales

    @property
    def lineas_conectadas(self) -> dict:
        return self.__lineas_conectadas

    @lineas_conectadas.setter
    def lineas_conectadas(self, lineas_conectadas: dict) -> None:
        self.__lineas_conectadas = lineas_conectadas

    def enviar_datos_API(self) -> None:
        url: str = 'http://192.168.100.61:3001/apiv1.0/IoT/pruebas'
        datos: dict = {
            'linea': self.__id_linea,
        }
        zonas: dict = dict()

        for id_zona in self.elementos:
            zona = self.elementos[id_zona]
            zonas[id_zona] = {
                'piezaDetectada': not zona.zona_libre(),
            }
            if not zona.zona_libre():
                zonas[id_zona]['tipoPieza'] = zona.pieza_en_zona.tipo_pieza.name
                zonas[id_zona]['dataMatrix'] = zona.pieza_en_zona.data_matrix
                zonas[id_zona]['statusLeak'] = zona.pieza_en_zona.status_leak.name
                zonas[id_zona]['statusInspeccion'] = zona.pieza_en_zona.status.name

        datos['zonas'] = zonas

        respuesta = requests.post(url, json=datos)
        respuesta.close()

    def generar_cola_actualizacion(self) -> list:
        # Realiza un recorrido DFS para generar la cola de actualizacion.
        self.__cola_actualizacion.append(
            self.DFS(self.__zona_inicial, self.__cola_actualizacion)
        )

    def conectar_lineas(self) -> None:
        for id_zona_conecta in self.__lineas_conectadas:
            self.elementos[
                id_zona_conecta
            ].conexion_con_linea = self.__lineas_conectadas[id_zona_conecta]

    def zona_inicial_libre(self) -> bool:
        return self.elementos[self.__zona_inicial].zona_libre()

    def push_pieza(self, pieza: Pieza) -> None:
        if pieza is not None:
            if self.elementos[self.__zona_inicial].zona_libre():
                self.elementos[self.__zona_inicial].ingresar_pieza(pieza)

    def pop_pieza(self, id_zona: str) -> Pieza:
        if self.elemento_es_hoja(id_zona):
            zona = self.elementos[id_zona]
            return zona.mover_pieza()

        return None

    def update(self, frame_count: int) -> None:
        zonas_actualizadas = []
        for id_zona in self.__cola_actualizacion:
            if id_zona not in zonas_actualizadas:
                zonas_actualizadas.append(id_zona)
                zona = self.elementos[id_zona]
                evento_emitido = zona.step(self)

                if evento_emitido is not None:
                    emisor, evento = evento_emitido
                    self.__cola_eventos[emisor] = evento

        for id_zona in self.elementos:
            zona = self.elementos[id_zona]
            zona.procesar_eventos(self.__cola_eventos)

        if self.__temporizador_request.en_espera():
            self.__temporizador_request.update()
        else:
            self.enviar_datos_API()
            self.__temporizador_request.reset()