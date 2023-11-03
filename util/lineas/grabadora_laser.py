import random
from datetime import datetime

from ..db_manager import Dbm
from ..clases.lineas.linea import Linea
from ..clases.piezas.pieza import Pieza
from ..clases.piezas.status import STATUS
from ..clases.controladores.plc import Plc
from ..clases.controladores.reportes import TIPO_REPORTE
from ..clases.piezas.tipos import TIPO_PIEZA
from ..clases.controladores.reportes import TIPO_REPORTE
from ..clases.zonas.estacion import Estacion
from ..clases.zonas.conveyor import Conveyor

class Grabadora_Laser(Linea):

    def __init__(
        self,
        database_manager: Dbm,
        linea_leak_tester: Linea
    ) -> None:        
        # ID de la linea.
        self.__id_linea: str = 'linea_grabadora_lazer'

        # Simulador del plc de la linea.
        self.__plc: Plc = Plc('plc_0', database_manager)

        # Zona inicial de la linea.
        self.__zona_inicial: str = 'conveyor_1'

        # Zonas finales de la linea.
        self.__zonas_finales: list[str] = ['conveyor_4']

        # Topologia de la linea.
        self.__topologia: dict = {
            'conveyor_1':  ['conveyor_2'],
            'conveyor_2':  ['grabadora_lazer'],
            'grabadora_lazer': ['conveyor_3'],
            'conveyor_3':  ['conveyor_4'],
            'conveyor_4':  [],
        }

        # Componentes de la topologia.
        self.__zonas: dict = {
            'conveyor_1': Conveyor('conveyor_1', posicion=(0,0)),
            'conveyor_2': Conveyor('conveyor_2', posicion=(1,0)),
            'grabadora_lazer': Estacion(
                'grabadora_lazer',
                self.grabar_data_matrix,
                posicion=(2,0)
            ),
            'conveyor_3': Conveyor('conveyor_3', posicion=(3,0)),
            'conveyor_4': Conveyor('conveyor_4', posicion=(4,0)),
        }

        # Conexiones con otras lineas.
        self.__lineas_conectadas: dict = {
            'conveyor_4': (
                linea_leak_tester,
                'conveyor_1'
            )
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
            'Linea grabadora de Data Matrix a piezas por medio de laser'
        )

    def grabar_data_matrix(self, estacion: Estacion, pieza: Pieza) -> None:
        hoy = datetime.today()
        pieza.tipo_pieza = random.choice([*TIPO_PIEZA][1:])

        pieza.data_matrix = '{}{}{}{}{}{}{}{}'.format(
            pieza.tipo_pieza.value,
            hoy.year,
            hoy.month,
            hoy.day,
            hoy.hour,
            hoy.minute,
            hoy.second,
            hoy.microsecond
        )

        pieza.set_status(
            leak_test=STATUS.INDEFINIDA,
            final_test=STATUS.INDEFINIDA
        )

        self.plc.database_manager.iniciar_tracking(pieza, self.id, estacion.id)

        self.plc.database_manager.generar_reporte(
            'Datamatrix grabado en pieza',
            pieza.data_matrix,
            '{}_{}'.format(self.id, estacion.id),
            TIPO_REPORTE.DATA_MATRX_GRABADO.name
        )