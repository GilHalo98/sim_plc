class Temporizador():

    def __init__(
        self,
        frames_espera: int
    ) -> None:
        '''
            Temporizador para esperar una cantidad de frames dada.
        '''

        # Frames que espera el temporizador.
        self.__frames_espera: int = frames_espera

        # Conteo de frames actual.
        self.__conteo: int = 1

    @property
    def conteo(self) -> int:
        return self.__conteo

    def reset(self) -> None:
        # Resetea el contador a 1.
        self.__conteo = 1

    def en_espera(self) -> bool:
        # Indica si el contador esta en espera para terminar el conteo.
        return False if self.__conteo % self.__frames_espera == 0 else True

    def update(self) -> None:
        # Actualiza el conteo del contador.
        self.__conteo += 1 if self.en_espera() else 0