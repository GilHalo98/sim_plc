import os

import pygame

from util.db_manager import Dbm_API as Dbm
from util.gui.ventana import Ventana
from util.clases.piezas.pieza import Pieza
from util.clases.piezas.status import STATUS
from util.clases.piezas.tipos import TIPO_PIEZA
from util.clases.controladores.reportes import TIPO_REPORTE
from util.lineas.leak_tester import Leak_Tester
from util.lineas.inspeccion_seis import Inspeccion_Seis
from util.lineas.grabadora_laser import Grabadora_Laser
from util.lineas.inspeccion_cuatro import Inspeccion_Cuatro


def main() -> None:
    db_manager: Dbm = Dbm('temp.db')

    linea_inspeccion_4 = Inspeccion_Cuatro(
        db_manager
    )

    linea_inspeccion_6 = Inspeccion_Seis(
        db_manager
    )
    
    linea_leak_tester = Leak_Tester(
        db_manager,
        linea_inspeccion_4,
        linea_inspeccion_6
    )

    linea_grabadora_laser = Grabadora_Laser(
        db_manager,
        linea_leak_tester
    )

    lineas: list = [
        linea_grabadora_laser,
        linea_leak_tester,
        linea_inspeccion_4,
        linea_inspeccion_6
    ]

    db_manager.registrar_lineas(*lineas)
    db_manager.registrar_tipos_piezas(*TIPO_PIEZA)
    db_manager.registrar_estados_status(*STATUS)
    db_manager.registrar_tipos_status(['leak_test', 'final_test'])
    db_manager.registrar_tipos_reportes(*TIPO_REPORTE)

    db_manager.start()

    id_conteo = 1

    ventana: Ventana = Ventana()

    ventana.add_to_draw_buffer(
        *lineas
    )

    while ventana.ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ventana.ejecutando = False

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_w:
                    if lineas[0].push_pieza(Pieza(id_conteo)):
                        id_conteo += 1

        ventana.update()
        pygame.display.flip()
        ventana.reloj.tick(60)

    pygame.quit()
    db_manager.kill()


if __name__ == '__main__':
    os.system('clear')
    main()