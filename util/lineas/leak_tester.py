import random

from ..db_manager import Dbm
from ..clases.lineas.linea import Linea
from ..clases.piezas.pieza import Pieza
from ..clases.piezas.status import STATUS
from ..clases.controladores.plc import Plc
from ..clases.controladores.reportes import TIPO_REPORTE
from ..clases.zonas.eventos import EVENTOS
from ..clases.piezas.tipos import TIPO_PIEZA
from ..clases.zonas.estacion import Estacion
from ..clases.zonas.conveyor import Conveyor
from ..clases.zonas.brazo_robotico import Brazo_Robotico

class Leak_Tester(Linea):

    def __init__(
        self,
        database_manager: Dbm,
        linea_final_cuatro_cilindros: Linea,
        linea_final_seis_cilindros: Linea
        ) -> None:
        # ID de la linea.
        self.__id_linea: str = 'linea_leak_tester'

        # Simulador del plc de la linea.
        self.__plc: Plc = Plc('plc_1', database_manager)

        # Zona inicial de la linea.
        self.__zona_inicial: str = 'conveyor_1'

        # Zonas finales de la linea.
        self.__zonas_finales: list[str] = [
            'conveyor_cuatro_cilindros_4',
            'conveyor_seis_cilindros_4'
        ]

        # Topologia de la linea.
        self.__topologia: dict = {
            'conveyor_1':  ['conveyor_2'],
            'conveyor_2':  ['conveyor_3'],
            'conveyor_3':  ['conveyor_4'],
            'conveyor_4':  ['brazo_robotico'],
            'brazo_robotico': [
                'estacion_pruebas_1',
                'conveyor_cuatro_cilindros_1',
                'conveyor_seis_cilindros_1',
                'conveyor_rechazo_cuatro_cilindros_1',
                'conveyor_rechazo_seis_cilindros_1'
            ],
            'estacion_pruebas_1': ['brazo_robotico'],
            'conveyor_cuatro_cilindros_1': ['conveyor_cuatro_cilindros_2'],
            'conveyor_cuatro_cilindros_2': ['conveyor_cuatro_cilindros_3'],
            'conveyor_cuatro_cilindros_3': ['conveyor_cuatro_cilindros_4'],
            'conveyor_cuatro_cilindros_4': [],
            'conveyor_rechazo_cuatro_cilindros_1': [
                'conveyor_rechazo_cuatro_cilindros_2'
            ],
            'conveyor_rechazo_cuatro_cilindros_2': [
                'conveyor_rechazo_cuatro_cilindros_3'
            ],
            'conveyor_rechazo_cuatro_cilindros_3': [
                'conveyor_rechazo_cuatro_cilindros_4'
            ],
            'conveyor_rechazo_cuatro_cilindros_4': [],
            'conveyor_seis_cilindros_1': ['conveyor_seis_cilindros_2'],
            'conveyor_seis_cilindros_2': ['conveyor_seis_cilindros_3'],
            'conveyor_seis_cilindros_3': ['conveyor_seis_cilindros_4'],
            'conveyor_seis_cilindros_4': [],
            'conveyor_rechazo_seis_cilindros_1': [
                'conveyor_rechazo_seis_cilindros_2'
            ],
            'conveyor_rechazo_seis_cilindros_2': [
                'conveyor_rechazo_seis_cilindros_3'
            ],
            'conveyor_rechazo_seis_cilindros_3': [
                'conveyor_rechazo_seis_cilindros_4'
            ],
            'conveyor_rechazo_seis_cilindros_4': [],
        }

        # Componentes de la topologia.
        self.__zonas: dict = {
            'conveyor_1': Conveyor('conveyor_1', posicion=(4,1)),
            'conveyor_2': Conveyor('conveyor_2', posicion=(4,2)),
            'conveyor_3': Conveyor('conveyor_3', posicion=(4,3)),
            'conveyor_4': Conveyor('conveyor_4', posicion=(4,4)),
            'brazo_robotico': Brazo_Robotico(
                'brazo_robotico',
                self.evaluacion_pieza_brazo_robotico,
                posicion=(4,5)
            ),
            'estacion_pruebas_1': Estacion(
                'estacion_pruebas_1',
                self.evaluacion_leak,
                posicion=(5,6)
            ),
            'conveyor_cuatro_cilindros_1': Conveyor(
                'conveyor_cuatro_cilindros_1',
                posicion=(5,5)
            ),
            'conveyor_cuatro_cilindros_2': Conveyor(
                'conveyor_cuatro_cilindros_2',
                posicion=(6,5)
            ),
            'conveyor_cuatro_cilindros_3': Conveyor(
                'conveyor_cuatro_cilindros_3',
                posicion=(7,5)
            ),
            'conveyor_cuatro_cilindros_4': Conveyor(
                'conveyor_cuatro_cilindros_4',
                posicion=(8,5)
            ),
            'conveyor_seis_cilindros_1': Conveyor(
                'conveyor_seis_cilindros_1',
                posicion=(4,6)
            ),
            'conveyor_seis_cilindros_2': Conveyor(
                'conveyor_seis_cilindros_2',
                posicion=(4,7)
            ),
            'conveyor_seis_cilindros_3': Conveyor(
                'conveyor_seis_cilindros_3',
                posicion=(4,8)
            ),
            'conveyor_seis_cilindros_4': Conveyor(
                'conveyor_seis_cilindros_4',
                posicion=(4,9)
            ),
            'conveyor_rechazo_cuatro_cilindros_1': Conveyor(
                'conveyor_rechazo_cuatro_cilindros_1',
                posicion=(3,5)
            ),
            'conveyor_rechazo_cuatro_cilindros_2': Conveyor(
                'conveyor_rechazo_cuatro_cilindros_2',
                posicion=(2,5)
            ),
            'conveyor_rechazo_cuatro_cilindros_3': Conveyor(
                'conveyor_rechazo_cuatro_cilindros_3',
                posicion=(1,5)
            ),
            'conveyor_rechazo_cuatro_cilindros_4': Conveyor(
                'conveyor_rechazo_cuatro_cilindros_4',
                posicion=(0,5)
            ),
            'conveyor_rechazo_seis_cilindros_1': Conveyor(
                'conveyor_rechazo_seis_cilindros_1',
                posicion=(3,6)
            ),
            'conveyor_rechazo_seis_cilindros_2': Conveyor(
                'conveyor_rechazo_seis_cilindros_2',
                posicion=(2,6)
            ),
            'conveyor_rechazo_seis_cilindros_3': Conveyor(
                'conveyor_rechazo_seis_cilindros_3',
                posicion=(1,6)
            ),
            'conveyor_rechazo_seis_cilindros_4': Conveyor(
                'conveyor_rechazo_seis_cilindros_4',
                posicion=(0,6)
            ),
        }

        # Conexiones con otras lineas.
        self.__lineas_conectadas: dict = {
            'conveyor_cuatro_cilindros_4': (
                linea_final_cuatro_cilindros,
                'conveyor_1'
            ),
            'conveyor_seis_cilindros_4': (
                linea_final_seis_cilindros,
                'conveyor_1'
            ),
        }

        # Inicializamos la clase padre.
        super().__init__(
            self.__id_linea,
            self.__plc,
            self.__zona_inicial,
            self.__zonas_finales,
            self.__topologia,
            self.__zonas,
            self.__lineas_conectadas,
            'Linea de evaluacion de pieza, verifica que no existan fugas en la chaqueta de agua del bloque del motor'
        )

    def evaluacion_leak(self, estacion: Estacion, pieza: Pieza) -> tuple:
        tipo_reporte = TIPO_REPORTE.INDEFINIDO.name

        if pieza.data_matrix is None:
            pieza.status['leak_test'] = STATUS.NO_DATA_MATRIX
            tipo_reporte = TIPO_REPORTE.NO_DATA_MATRIX_DETECTADA.name

        else:
            pieza.status['leak_test'] = random.choice([
                STATUS.OK,
                STATUS.RECHAZADA
            ])

            if pieza.status['leak_test'] is STATUS.OK:
                tipo_reporte = TIPO_REPORTE.INSPECCION_LEAK_OK.name

            else:
                tipo_reporte = TIPO_REPORTE.INSPECCION_LEAK_RECHAZO.name

        self.plc.database_manager.generar_reporte(
            'Pruebas de chaqueta de agua realizada en pieza',
            pieza.data_matrix,
            '{}_{}'.format(self.id, estacion.id),
            tipo_reporte
        )

        return (
            'estacion_pruebas_1',
            EVENTOS.TERMINA_ESPERA
        )


    def evaluacion_pieza_brazo_robotico(
        self,
        robot: Brazo_Robotico,
        pieza: Pieza,
        iniciar_esperas: bool
    ) -> int:
        if pieza.status['leak_test'] is STATUS.INDEFINIDA:
            if iniciar_esperas:
                robot.iniciar_espera_por_evento(
                    'estacion_pruebas_1',
                    EVENTOS.TERMINA_ESPERA
                )

            return 0

        else:
            if pieza.tipo_pieza is TIPO_PIEZA.CUATRO_CILINDROS:
                return 1 if pieza.status['leak_test'] is STATUS.OK else 3

            elif pieza.tipo_pieza is TIPO_PIEZA.SEIS_CILINDROS:
                return 2 if pieza.status['leak_test'] is STATUS.OK else 4