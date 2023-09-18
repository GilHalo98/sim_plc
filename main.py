import os
import time
import random
import pathlib

from util.clases.lineas.linea import Linea
from util.clases.zonas.conveyor import Conveyor
from util.clases.zonas.estacion import Estacion
from util.clases.zonas.tornamesa import Tornamesa
from util.clases.zonas.brazo_robotico import Brazo_Robotico
from util.clases.piezas.pieza import Pieza
from util.clases.piezas.status import STATUS
from util.clases.piezas.tipos import TIPO_PIEZA
from util.clases.zonas.eventos import EVENTOS
from util.graficador import graficar_linea


def evaluacion_pieza_tornamesa(
    tornamesa: Tornamesa,
    pieza: Pieza,
    iniciar_esperas: bool
) -> int:
    if pieza.status is not STATUS.OK:
        return 0

    return 1


def evaluacion_pieza_brazo_robotico(
    robot: Brazo_Robotico,
    pieza: Pieza,
    iniciar_esperas: bool
) -> int:
    if pieza.status_leak is STATUS.INDEFINIDA:
        if iniciar_esperas:
            robot.iniciar_espera_por_evento('estacion_pruebas_1', EVENTOS.TERMINA_ESPERA)

        return 0

    else:
        if pieza.tipo_pieza is TIPO_PIEZA.CUATRO_CILINDROS:
            return 1 if pieza.status_leak is STATUS.OK else 3

        elif pieza.tipo_pieza is TIPO_PIEZA.SEIS_CILINDROS:
            return 2 if pieza.status_leak is STATUS.OK else 4


def evaluacion_leak(estacion: Estacion, pieza: Pieza) -> tuple:
    if pieza.data_matrix is None:
        pieza.status_leak = STATUS.NO_DATA_MATRIX

    else:
        pieza.status_leak = random.choice([
            STATUS.OK,
            STATUS.RECHAZADA
        ])

    return (
        'estacion_pruebas_1',
        EVENTOS.TERMINA_ESPERA
    )


def procesar_pieza_inspeccion(estacion: Estacion, pieza: Pieza) -> None:
    if pieza.data_matrix is None:
        pieza.status = STATUS.NO_DATA_MATRIX

    else:
        pieza.status = random.choice([
            STATUS.OK,
            STATUS.RECHAZADA
        ])


def grabar_data_matrix(estacion: Estacion, pieza: Pieza) -> None:
    data_matrix = random.randint(1e3, 9e3)
    pieza.data_matrix = '{}'.format(data_matrix)
    pieza.tipo_pieza = random.choice([*TIPO_PIEZA][1:])


def main() -> None:

    linea_final_seis_cilindros: Linea = Linea(
        'linea_final_seis_cilindros',
        'conveyor_1',
        ['rechazo_3', 'conveyor_7', 'rechazo_6'],
        {
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
        },
        {
            'conveyor_1': Conveyor('conveyor_1'),
            'estacion_1': Estacion('estacion_1', procesar_pieza_inspeccion, frames_proceso=60),
            'conveyor_2': Conveyor('conveyor_2'),
            'tornamesa_1': Tornamesa('tornamesa_1', evaluacion_pieza_tornamesa),
            'rechazo_1': Conveyor('rechazo_1'),
            'rechazo_2': Conveyor('rechazo_2'),
            'rechazo_3': Conveyor('rechazo_3'),
            'conveyor_3': Conveyor('conveyor_3'),
            'estacion_2': Estacion('estacion_2', procesar_pieza_inspeccion, frames_proceso=60),
            'conveyor_4': Conveyor('conveyor_4'),
            'tornamesa_2': Tornamesa('tornamesa_2', evaluacion_pieza_tornamesa),
            'conveyor_5': Conveyor('conveyor_5'),
            'conveyor_6': Conveyor('conveyor_6'),
            'conveyor_7': Conveyor('conveyor_7'),
            'rechazo_4': Conveyor('rechazo_4'),
            'rechazo_5': Conveyor('rechazo_5'),
            'rechazo_6': Conveyor('rechazo_6'),
        },
    )

    linea_final_cuatro_cilindros: Linea = Linea(
        'linea_final_cuatro_cilindros',
        'conveyor_1',
        ['rechazo_3', 'conveyor_7', 'rechazo_6'],
        {
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
        },
        {
            'conveyor_1': Conveyor('conveyor_1'),
            'estacion_1': Estacion('estacion_1', procesar_pieza_inspeccion, frames_proceso=60),
            'conveyor_2': Conveyor('conveyor_2'),
            'tornamesa_1': Tornamesa('tornamesa_1', evaluacion_pieza_tornamesa),
            'rechazo_1': Conveyor('rechazo_1'),
            'rechazo_2': Conveyor('rechazo_2'),
            'rechazo_3': Conveyor('rechazo_3'),
            'conveyor_3': Conveyor('conveyor_3'),
            'estacion_2': Estacion('estacion_2', procesar_pieza_inspeccion, frames_proceso=60),
            'conveyor_4': Conveyor('conveyor_4'),
            'tornamesa_2': Tornamesa('tornamesa_2', evaluacion_pieza_tornamesa),
            'conveyor_5': Conveyor('conveyor_5'),
            'conveyor_6': Conveyor('conveyor_6'),
            'conveyor_7': Conveyor('conveyor_7'),
            'rechazo_4': Conveyor('rechazo_4'),
            'rechazo_5': Conveyor('rechazo_5'),
            'rechazo_6': Conveyor('rechazo_6'),
        },
    )

    linea_leak_tester: Linea = Linea(
        'linea_leak_tester',
        'conveyor_1',
        ['conveyor_cuatro_cilindros_4', 'conveyor_seis_cilindros_4'],
        {
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
            'conveyor_rechazo_cuatro_cilindros_1': ['conveyor_rechazo_cuatro_cilindros_2'],
            'conveyor_rechazo_cuatro_cilindros_2': ['conveyor_rechazo_cuatro_cilindros_3'],
            'conveyor_rechazo_cuatro_cilindros_3': ['conveyor_rechazo_cuatro_cilindros_4'],
            'conveyor_rechazo_cuatro_cilindros_4': [],
            'conveyor_seis_cilindros_1': ['conveyor_seis_cilindros_2'],
            'conveyor_seis_cilindros_2': ['conveyor_seis_cilindros_3'],
            'conveyor_seis_cilindros_3': ['conveyor_seis_cilindros_4'],
            'conveyor_seis_cilindros_4': [],
            'conveyor_rechazo_seis_cilindros_1': ['conveyor_rechazo_seis_cilindros_2'],
            'conveyor_rechazo_seis_cilindros_2': ['conveyor_rechazo_seis_cilindros_3'],
            'conveyor_rechazo_seis_cilindros_3': ['conveyor_rechazo_seis_cilindros_4'],
            'conveyor_rechazo_seis_cilindros_4': [],
        },
        {
            'conveyor_1': Conveyor('conveyor_1'),
            'conveyor_2': Conveyor('conveyor_2'),
            'conveyor_3': Conveyor('conveyor_3'),
            'conveyor_4': Conveyor('conveyor_4'),
            'brazo_robotico': Brazo_Robotico('brazo_robotico', evaluacion_pieza_brazo_robotico),
            'estacion_pruebas_1': Estacion('estacion_pruebas_1', evaluacion_leak),
            'conveyor_cuatro_cilindros_1': Conveyor('conveyor_cuatro_cilindros_1'),
            'conveyor_cuatro_cilindros_2': Conveyor('conveyor_cuatro_cilindros_2'),
            'conveyor_cuatro_cilindros_3': Conveyor('conveyor_cuatro_cilindros_3'),
            'conveyor_cuatro_cilindros_4': Conveyor('conveyor_cuatro_cilindros_4'),
            'conveyor_seis_cilindros_1': Conveyor('conveyor_seis_cilindros_1'),
            'conveyor_seis_cilindros_2': Conveyor('conveyor_seis_cilindros_2'),
            'conveyor_seis_cilindros_3': Conveyor('conveyor_seis_cilindros_3'),
            'conveyor_seis_cilindros_4': Conveyor('conveyor_seis_cilindros_4'),
            'conveyor_rechazo_cuatro_cilindros_1': Conveyor('conveyor_rechazo_cuatro_cilindros_1'),
            'conveyor_rechazo_cuatro_cilindros_2': Conveyor('conveyor_rechazo_cuatro_cilindros_2'),
            'conveyor_rechazo_cuatro_cilindros_3': Conveyor('conveyor_rechazo_cuatro_cilindros_3'),
            'conveyor_rechazo_cuatro_cilindros_4': Conveyor('conveyor_rechazo_cuatro_cilindros_4'),
            'conveyor_rechazo_seis_cilindros_1': Conveyor('conveyor_rechazo_seis_cilindros_1'),
            'conveyor_rechazo_seis_cilindros_2': Conveyor('conveyor_rechazo_seis_cilindros_2'),
            'conveyor_rechazo_seis_cilindros_3': Conveyor('conveyor_rechazo_seis_cilindros_3'),
            'conveyor_rechazo_seis_cilindros_4': Conveyor('conveyor_rechazo_seis_cilindros_4'),
        },
        {
            'conveyor_cuatro_cilindros_4': (linea_final_cuatro_cilindros, 'conveyor_1'),
            'conveyor_seis_cilindros_4': (linea_final_seis_cilindros, 'conveyor_1'),
        }
    )

    linea_grabadora_lazer: Linea = Linea(
        'linea_grabadora_lazer',
        'conveyor_1',
        ['conveyor_4'],
        {
            'conveyor_1':  ['conveyor_2'],
            'conveyor_2':  ['grabadora_lazer'],
            'grabadora_lazer': ['conveyor_3'],
            'conveyor_3':  ['conveyor_4'],
            'conveyor_4':  [],
        },
        {
            'conveyor_1': Conveyor('conveyor_1'),
            'conveyor_2': Conveyor('conveyor_2'),
            'grabadora_lazer': Estacion('grabadora_lazer', grabar_data_matrix),
            'conveyor_3': Conveyor('conveyor_3'),
            'conveyor_4': Conveyor('conveyor_4'),
        },
        {
            'conveyor_4': (linea_leak_tester, 'conveyor_1')
        }
    )

    lineas: list = [
        linea_grabadora_lazer,
        linea_leak_tester,
        linea_final_seis_cilindros,
        linea_final_cuatro_cilindros
    ]

    for linea in lineas:
        graficar_linea(linea, pathlib.Path('graficos/' + str(linea.id)))

    frame_count = 1
    conteo_id = 0
    while True:
        if frame_count % 1 == 0:
            os.system('clear')

            print('-'*20 + '| frame {} |'.format(frame_count) + '-'*20)

            for linea in lineas:
                print(linea)

        if frame_count % 5 == 0:
            if random.random() < 0.2 and lineas[0].zona_inicial_libre():
                lineas[0].push_pieza(Pieza(conteo_id))
                conteo_id += 1

        for linea in lineas:
            linea.update(frame_count)

        time.sleep(0.05)
        frame_count += 1


if __name__ == '__main__':
    os.system('clear')
    main()
