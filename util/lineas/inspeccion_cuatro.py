import random

from ..db_manager import Dbm
from ..clases.lineas.linea import Linea
from ..clases.piezas.pieza import Pieza
from ..clases.piezas.status import STATUS
from ..clases.controladores.plc import Plc
from ..clases.controladores.reportes import TIPO_REPORTE
from ..clases.piezas.tipos import TIPO_PIEZA
from ..clases.zonas.estacion import Estacion
from ..clases.zonas.conveyor import Conveyor
from ..clases.zonas.tornamesa import Tornamesa

class Inspeccion_Cuatro(Linea):

    def __init__(
        self,
        database_manager: Dbm
    ) -> None:        
        # ID de la linea.
        self.__id_linea: str = 'linea_final_cuatro_cilindros'

        # Simulador del plc de la linea.
        self.__plc: Plc = Plc('plc_3', database_manager)

        # Zona inicial de la linea.
        self.__zona_inicial: str = 'conveyor_1'

        # Zonas finales de la linea.
        self.__zonas_finales: list[str] = [
            'rechazo_3',
            'conveyor_7',
            'rechazo_6'
        ]

        # Topologia de la linea.
        self.__topologia: dict = {
            'conveyor_1':  ['estacion_1'],
            'estacion_1':  ['conveyor_2'],
            'conveyor_2':  ['tornamesa_1'],
            'tornamesa_1':  ['rechazo_1', 'conveyor_3'],
            'rechazo_1': ['rechazo_2'],
            'rechazo_2': ['rechazo_3'],
            'rechazo_3': [],
            'conveyor_3': ['estacion_2'],
            'estacion_2': ['conveyor_4'],
            'conveyor_4': ['tornamesa_2'],
            'tornamesa_2':  ['rechazo_4', 'conveyor_5'],
            'conveyor_5': ['conveyor_6'],
            'conveyor_6': ['conveyor_7'],
            'conveyor_7': [],
            'rechazo_4': ['rechazo_5'],
            'rechazo_5': ['rechazo_6'],
            'rechazo_6': [],
        }

        # Componentes de la topologia.
        self.__zonas: dict = {
            'conveyor_1': Conveyor('conveyor_1', posicion=(9,5)),
            'estacion_1': Estacion(
                'estacion_1',
                self.procesar_pieza_inspeccion,
                frames_proceso=60, posicion=(10,5)
            ),
            'conveyor_2': Conveyor('conveyor_2', posicion=(11,5)),
            'tornamesa_1': Tornamesa(
                'tornamesa_1',
                self.evaluacion_pieza_tornamesa,
                posicion=(12,5)
            ),
            'rechazo_1': Conveyor('rechazo_1', posicion=(12,6)),
            'rechazo_2': Conveyor('rechazo_2', posicion=(12,7)),
            'rechazo_3': Conveyor('rechazo_3', posicion=(12,8)),
            'conveyor_3': Conveyor('conveyor_3', posicion=(13,5)),
            'estacion_2': Estacion(
                'estacion_2',
                self.procesar_pieza_inspeccion,
                frames_proceso=60,
                posicion=(14,5)
            ),
            'conveyor_4': Conveyor('conveyor_4', posicion=(15,5)),
            'tornamesa_2': Tornamesa(
                'tornamesa_2',
                self.evaluacion_pieza_tornamesa,
                posicion=(16,5)
            ),
            'conveyor_5': Conveyor('conveyor_5', posicion=(17,5)),
            'conveyor_6': Conveyor('conveyor_6', posicion=(18,5)),
            'conveyor_7': Conveyor('conveyor_7', posicion=(19,5)),
            'rechazo_4': Conveyor('rechazo_4', posicion=(16,6)),
            'rechazo_5': Conveyor('rechazo_5', posicion=(16,7)),
            'rechazo_6': Conveyor('rechazo_6', posicion=(16,8)),
        }

        # Conexiones con otras lineas.
        self.__lineas_conectadas: dict = dict()

        # Inicializamos la clase padre.
        super().__init__(
            self.__id_linea,
            self.__plc,
            self.__zona_inicial,
            self.__zonas_finales,
            self.__topologia,
            self.__zonas,
            self.__lineas_conectadas,
            'Linea de inspección de bloque de motor de cuatro cilindros'
        )

    def evaluacion_pieza_tornamesa(
        self,
        tornamesa: Tornamesa,
        pieza: Pieza,
        iniciar_esperas: bool
    ) -> int:
        if pieza.status['final_test'] is not STATUS.OK:
            return 0

        return 1

    def procesar_pieza_inspeccion(
        self,
        estacion: Estacion,
        pieza: Pieza
    ) -> None:
        tipo_reporte = TIPO_REPORTE.INDEFINIDO.name

        if pieza.data_matrix is None:
            pieza.status['final_test'] = STATUS.NO_DATA_MATRIX
            tipo_reporte = TIPO_REPORTE.NO_DATA_MATRIX_DETECTADA.name

        else:
            pieza.status['final_test'] = random.choice([
                STATUS.OK,
                STATUS.RECHAZADA
            ])

            if pieza.status['final_test'] is STATUS.OK:
                tipo_reporte = TIPO_REPORTE.INSPECCION_FINAL_OK.name

            else:
                tipo_reporte = TIPO_REPORTE.INSPECCION_FINAL_RECHAZO.name
            
        self.plc.database_manager.generar_reporte(
            'Inspeccion de calidad realizada en pieza',
            pieza.data_matrix,
            '{}_{}'.format(self.id, estacion.id),
            tipo_reporte
        )

