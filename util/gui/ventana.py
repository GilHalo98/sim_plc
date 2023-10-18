import random
import pygame
from ..clases.zonas.tipos import TIPO_ZONA
from ..temporizador import Temporizador


class Ventana():
    def __init__(self) -> None:
        pygame.init()
        self.canvas = pygame.display.set_mode((1020, 540))
        self.reloj = pygame.time.Clock()
        self.ejecutando = True
        self.dim_mesh = (22, 22)
        self.dim_bloques = self.__determinar_dim_bloques()
        self.frame_count = 0
        self.buffer = list()
        self.colores_lineas = dict()
        self.cursor_en_zona: Zona | None = None
        self.cursor_en_linea: Linea | None = None
        self.temporizador_click = Temporizador(10)

    def __determinar_dim_bloques(self) -> tuple[int, int]:
        dim_bloques = (
            int(self.canvas.get_size()[0] / self.dim_mesh[0]),
            int(self.canvas.get_size()[1] / self.dim_mesh[1])
        )

        return dim_bloques

    def __dibuja_mesh(self) -> None:
        y = 0
        x = 0

        for _ in range(self.dim_mesh[1]):
            x = 0
            for _ in range(self.dim_mesh[0]):
                celda = pygame.Rect(
                    (x, y),
                    (self.dim_bloques[0], self.dim_bloques[1])
                )

                cursor_en_celda: bool = celda.collidepoint(
                    pygame.mouse.get_pos()
                )

                color_celda: tuple[int, int, int] = (0, 0, 0)

                if cursor_en_celda:
                    color_celda = (0, 255, 255)
                    self.cursor_en_zona = None
                    self.cursor_en_linea = None

                pygame.draw.rect(
                        self.canvas,
                        color_celda,
                        celda,
                        1
                )
                x += self.dim_bloques[0]
            y += self.dim_bloques[1]

    def __render_buffer(self) -> None:
        for linea in self.buffer:
            for id_zona in linea.elementos:
                zona = linea.elementos[id_zona]
                posicion = zona.posicion

                celda = pygame.Rect(
                    (
                        (self.dim_bloques[0] * posicion[0]) + 1,
                        (self.dim_bloques[1] * posicion[1]) + 1
                    ),
                    (self.dim_bloques[0] - 2, self.dim_bloques[1] - 2)
                )

                cursor_en_celda: bool = celda.collidepoint(
                    pygame.mouse.get_pos()
                )

                if cursor_en_celda:
                    if self.cursor_en_zona != None:
                        if self.cursor_en_zona.id != id_zona:
                            self.cursor_en_zona = linea.elementos[id_zona]
                            self.cursor_en_linea = linea
                        
                    else:
                        self.cursor_en_zona = linea.elementos[id_zona]
                        self.cursor_en_linea = linea

                pygame.draw.rect(
                        self.canvas,
                        self.colores_lineas[linea.id],
                        celda,
                )

                if zona.tipo_zona is TIPO_ZONA.CONVEYOR:
                    pygame.draw.rect(
                        self.canvas,
                        (0, 255, 0) if zona.zona_libre() else (255, 0, 0),
                        pygame.Rect(
                            (
                                (self.dim_bloques[0] * posicion[0]) + 9,
                                (self.dim_bloques[1] * posicion[1]) + 9
                            ),
                            (
                                self.dim_bloques[0] - 18,
                                self.dim_bloques[1] - 18
                            )
                        ),
                    )

                elif zona.tipo_zona is TIPO_ZONA.ESTACION:
                    pygame.draw.rect(
                        self.canvas,
                        (0, 255, 0) if zona.zona_libre() else (255, 0, 0),
                        pygame.Rect(
                            (
                                (self.dim_bloques[0] * posicion[0]) + 5,
                                (self.dim_bloques[1] * posicion[1]) + 5
                            ),
                            (
                                self.dim_bloques[0] - 10,
                                self.dim_bloques[1] - 10
                            )
                        ),
                    )

                else:
                    pygame.draw.circle(
                        self.canvas,
                        (0, 255, 0) if zona.zona_libre() else (255, 0, 0),
                        (
                            (self.dim_bloques[0] * posicion[0])
                                + (self.dim_bloques[0] /2),
                            (self.dim_bloques[1] * posicion[1])
                                + (self.dim_bloques[1] /2)
                        ),
                        9
                    )

    def add_to_draw_buffer(self, *lineas) -> None:
        '''
            Agrega lineas al buffer de renderizado.
        '''

        for linea in lineas:
            # Por cada linea se selecciona un color aleatorio.
            color_aleatorio: tuple[int, int, int] = (
                random.randint(50, 180),
                random.randint(50, 180),
                random.randint(50, 180),
            )

            # Se agrega al buffer.
            self.buffer.append(linea)

            # Se guarda el color seleccionado.
            self.colores_lineas[linea.id] = color_aleatorio

    def update(self) -> None:
        self.canvas.fill((0, 0, 0))
        self.__dibuja_mesh()
        self.__render_buffer()

        for linea in self.buffer:
            linea.update(self.frame_count)

        botones_precionados_mouse = pygame.mouse.get_pressed()
        if not self.temporizador_click.en_espera():
            if(
                botones_precionados_mouse[0]
                and self.cursor_en_linea != None
            ):
                pieza_removida: Pieza = self.cursor_en_linea.pop_pieza(
                    self.cursor_en_zona.id
                )

                print('Pieza Removida: {}'.format(pieza_removida))
                self.temporizador_click.reset()

            elif botones_precionados_mouse[2]:
                print(self.cursor_en_zona)
                self.temporizador_click.reset()
        else:
            self.temporizador_click.update()

        self.frame_count += 1