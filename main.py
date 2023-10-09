import os
import time
import random
import pathlib

import pygame

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
from util.gui.ventana import Ventana


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
            robot.iniciar_espera_por_evento(
                'estacion_pruebas_1',
                EVENTOS.TERMINA_ESPERA
            )

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
            'conveyor_1': Conveyor('conveyor_1', posicion=(4,10)),
            'estacion_1': Estacion(
                'estacion_1',
                procesar_pieza_inspeccion,
                frames_proceso=60,
                posicion=(4,11)
            ),
            'conveyor_2': Conveyor('conveyor_2', posicion=(4,12)),
            'tornamesa_1': Tornamesa(
                'tornamesa_1',
                evaluacion_pieza_tornamesa, posicion=(4,13)
            ),
            'rechazo_1': Conveyor('rechazo_1', posicion=(3,13)),
            'rechazo_2': Conveyor('rechazo_2', posicion=(2,13)),
            'rechazo_3': Conveyor('rechazo_3', posicion=(1,13)),

            'conveyor_3': Conveyor('conveyor_3', posicion=(4,14)),
            'estacion_2': Estacion(
                'estacion_2',
                procesar_pieza_inspeccion,
                frames_proceso=60,
                posicion=(4,15)
            ),
            'conveyor_4': Conveyor('conveyor_4', posicion=(4,16)),
            'tornamesa_2': Tornamesa(
                'tornamesa_2',
                evaluacion_pieza_tornamesa, posicion=(4,17)
            ),

            'conveyor_5': Conveyor('conveyor_5', posicion=(4,18)),
            'conveyor_6': Conveyor('conveyor_6', posicion=(4,19)),
            'conveyor_7': Conveyor('conveyor_7', posicion=(4,20)),
            'rechazo_4': Conveyor('rechazo_4', posicion=(3,17)),
            'rechazo_5': Conveyor('rechazo_5', posicion=(2,17)),
            'rechazo_6': Conveyor('rechazo_6', posicion=(1,17)),
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
            'conveyor_1': Conveyor('conveyor_1', posicion=(9,5)),
            'estacion_1': Estacion(
                'estacion_1',
                procesar_pieza_inspeccion,
                frames_proceso=60, posicion=(10,5)
            ),
            'conveyor_2': Conveyor('conveyor_2', posicion=(11,5)),
            'tornamesa_1': Tornamesa(
                'tornamesa_1',
                evaluacion_pieza_tornamesa,
                posicion=(12,5)
            ),
            'rechazo_1': Conveyor('rechazo_1', posicion=(12,6)),
            'rechazo_2': Conveyor('rechazo_2', posicion=(12,7)),
            'rechazo_3': Conveyor('rechazo_3', posicion=(12,8)),
            'conveyor_3': Conveyor('conveyor_3', posicion=(13,5)),
            'estacion_2': Estacion(
                'estacion_2',
                procesar_pieza_inspeccion,
                frames_proceso=60,
                posicion=(14,5)
            ),
            'conveyor_4': Conveyor('conveyor_4', posicion=(15,5)),
            'tornamesa_2': Tornamesa(
                'tornamesa_2',
                evaluacion_pieza_tornamesa,
                posicion=(16,5)
            ),
            'conveyor_5': Conveyor('conveyor_5', posicion=(17,5)),
            'conveyor_6': Conveyor('conveyor_6', posicion=(18,5)),
            'conveyor_7': Conveyor('conveyor_7', posicion=(19,5)),
            'rechazo_4': Conveyor('rechazo_4', posicion=(16,6)),
            'rechazo_5': Conveyor('rechazo_5', posicion=(16,7)),
            'rechazo_6': Conveyor('rechazo_6', posicion=(16,8)),
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
        },
        {
            'conveyor_1': Conveyor('conveyor_1', posicion=(4,1)),
            'conveyor_2': Conveyor('conveyor_2', posicion=(4,2)),
            'conveyor_3': Conveyor('conveyor_3', posicion=(4,3)),
            'conveyor_4': Conveyor('conveyor_4', posicion=(4,4)),
            'brazo_robotico': Brazo_Robotico(
                'brazo_robotico',
                evaluacion_pieza_brazo_robotico,
                posicion=(4,5)
            ),
            'estacion_pruebas_1': Estacion(
                'estacion_pruebas_1',
                evaluacion_leak,
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
        },
        {
            'conveyor_cuatro_cilindros_4': (
                linea_final_cuatro_cilindros,
                'conveyor_1'
            ),
            'conveyor_seis_cilindros_4': (
                linea_final_seis_cilindros,
                'conveyor_1'
            ),
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
            'conveyor_1': Conveyor('conveyor_1', posicion=(0,0)),
            'conveyor_2': Conveyor('conveyor_2', posicion=(1,0)),
            'grabadora_lazer': Estacion('grabadora_lazer', grabar_data_matrix, posicion=(2,0)),
            'conveyor_3': Conveyor('conveyor_3', posicion=(3,0)),
            'conveyor_4': Conveyor('conveyor_4', posicion=(4,0)),
        },
        {
            'conveyor_4': (linea_leak_tester, 'conveyor_1')
        }
    )

    id_conteo = 0

    ventana: Ventana = Ventana()

    ventana.buffer.append(
        linea_grabadora_lazer,
    )
    ventana.buffer.append(
        linea_leak_tester
    )

    ventana.buffer.append(
        linea_final_seis_cilindros
    )

    ventana.buffer.append(
        linea_final_cuatro_cilindros
    )

    while ventana.ejecutando:

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ventana.ejecutando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key== pygame.K_w:
                    id_conteo += 1
                    linea_grabadora_lazer.push_pieza(Pieza(id_conteo))


        ventana.update()
        pygame.display.flip()
        ventana.reloj.tick(60)

    pygame.quit()

if __name__ == '__main__':
    os.system('clear')
    main()
