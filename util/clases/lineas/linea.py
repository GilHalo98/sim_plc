from ..controladores.plc import Plc
from ...temporizador import Temporizador
from ...estructuras.grafo import Grafo
from ..piezas.pieza import Pieza
from ..zonas.tipos import TIPO_ZONA


class Linea(Grafo):
    def __init__(
        self,
        id_linea: str,
        plc: Plc,
        zona_inicial: str = None,
        zonas_finales: list = list(),
        conexiones: dict = dict(),
        zonas: dict = dict(),
        lineas_conectadas: dict = dict(),
        descripcion: str = ''
    ) -> None:
        # Inicializamos la clase padre, que este en caso es un grafo.
        super().__init__(conexiones, zonas)

        # ID de la linea.
        self.__id_linea: str = id_linea

        # Descripcion de la linea.
        self.__descripcion: str = descripcion

        # PLC controlador de la linea.
        self.__plc: Plc = plc

        # Zona inicial de la linea.
        self.__zona_inicial: str = zona_inicial

        # Lista de zonas finales de la linea.
        self.__zonas_finales: list =  zonas_finales

        # Diccionario de lineas interconectadas y en que zona final.
        self.__lineas_conectadas: dict = lineas_conectadas

        # Generamos la cola de actualizacion.
        self.__plc.generar_cola_actualizacion(self)

        # Conectamos la linea inicial con otras lineas.
        self.conectar_lineas()

    def __str__(self) -> str:
        msj = 'Linea {}:\n'
        msj += 'Eventos: {}\n'

        for id_zona in self.elementos:
            zona = self.elementos[id_zona]
            msj += str(zona) + '\n'

        return msj.format(self.__id_linea, self.__plc.cola_eventos)

    @property
    def id(self) -> str:
        return self.__id_linea
    
    @property
    def descripcion(self) -> str:
        return self.__descripcion

    @property
    def zona_inicial(self) -> str:
        return self.__zona_inicial

    @property
    def zonas_finales(self) -> list:
        return self.__zonas_finales

    @property
    def lineas_conectadas(self) -> dict:
        return self.__lineas_conectadas

    @property
    def plc(self) -> Plc:
        return self.__plc

    @descripcion.setter
    def descripcion(self, descripcion: str) -> None:
        self.__descripcion = descripcion

    @lineas_conectadas.setter
    def lineas_conectadas(self, lineas_conectadas: dict) -> None:
        self.__lineas_conectadas = lineas_conectadas

    def conectar_lineas(self) -> None:
        for id_zona_conecta in self.__lineas_conectadas:
            self.elementos[
                id_zona_conecta
            ].conexion_con_linea = self.__lineas_conectadas[
                id_zona_conecta
            ]

    def zona_inicial_libre(self) -> bool:
        return self.elementos[self.__zona_inicial].zona_libre()

    def push_pieza(self, pieza: Pieza) -> bool:
        if pieza is not None:
            if self.elementos[self.__zona_inicial].zona_libre():
                return self.elementos[
                    self.__zona_inicial
                ].ingresar_pieza(pieza)

        return False

    def pop_pieza(self, id_zona: str) -> Pieza:
        if self.elemento_es_hoja(id_zona):
            zona = self.elementos[id_zona]
            pieza: Pieza = zona.mover_pieza()
            if pieza != None:
                self.__plc.add_pieza_removida(pieza.data_matrix)
            return pieza

        return None

    def update(self, frame_count: int) -> None:
        self.__plc.update(self)