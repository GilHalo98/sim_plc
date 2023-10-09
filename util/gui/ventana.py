import pygame
from ..clases.zonas.tipos import TIPO_ZONA


class Ventana():
    def __init__(self) -> None:
        pygame.init()
        self.canvas = pygame.display.set_mode((1020, 540))
        self.reloj = pygame.time.Clock()
        self.ejecutando = True
        self.dim_mesh = (22, 22)
        self.dim_bloques = self.__determinar_dim_bloques()
        self.buffer = list()
        self.frame_count = 0

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
                pygame.draw.rect(
                        self.canvas,
                        (255, 255, 255),
                        pygame.Rect(
                            (x, y),
                            (self.dim_bloques[0], self.dim_bloques[1])
                        ),
                        1
                )
                x += self.dim_bloques[0]
            y += self.dim_bloques[1]

    def __render_buffer(self) -> None:
        for linea in self.buffer:
            for id_zona in linea.elementos:
                zona = linea.elementos[id_zona]
                posicion = zona.posicion

                pygame.draw.rect(
                        self.canvas,
                        (80, 80, 80),
                        pygame.Rect(
                            ((self.dim_bloques[0] * posicion[0]) + 1, (self.dim_bloques[1] * posicion[1]) + 1),
                            (self.dim_bloques[0] - 2, self.dim_bloques[1] - 2)
                        ),
                )

                if zona.tipo_zona is TIPO_ZONA.CONVEYOR:
                    pygame.draw.rect(
                        self.canvas,
                        (0, 255, 0) if zona.zona_libre() else (255, 0, 0),
                        pygame.Rect(
                            ((self.dim_bloques[0] * posicion[0]) + 9, (self.dim_bloques[1] * posicion[1]) + 9),
                            (self.dim_bloques[0] - 18, self.dim_bloques[1] - 18)
                        ),
                    )

                elif zona.tipo_zona is TIPO_ZONA.ESTACION:
                    pygame.draw.rect(
                        self.canvas,
                        (0, 255, 0) if zona.zona_libre() else (255, 0, 0),
                        pygame.Rect(
                            ((self.dim_bloques[0] * posicion[0]) + 5, (self.dim_bloques[1] * posicion[1]) + 5),
                            (self.dim_bloques[0] - 10, self.dim_bloques[1] - 10)
                        ),
                    )

                else:
                    pygame.draw.circle(
                        self.canvas,
                        (0, 255, 0) if zona.zona_libre() else (255, 0, 0),
                        (
                            (self.dim_bloques[0] * posicion[0]) + (self.dim_bloques[0] /2),
                            (self.dim_bloques[1] * posicion[1]) + (self.dim_bloques[1] /2)
                        ),
                        9
                    )

    def update(self) -> None:
        self.canvas.fill((0, 0, 0))
        self.__dibuja_mesh()
        self.__render_buffer()

        for linea in self.buffer:
            linea.update(self.frame_count)

        self.frame_count += 1