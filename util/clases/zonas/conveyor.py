from ..lineas.linea import Linea
from .zona import Zona
from .tipos import TIPO_ZONA


class Conveyor(Zona):
    def __init__(
        self,
        id: str,
        frames_movimiento: int = 160,
        posicion: tuple = None
    ) -> None:
        # Inicializamos la clase padre.
        super().__init__(
            id,
            TIPO_ZONA.CONVEYOR,
            frames_movimiento,
            posicion=posicion,
            descripcion='conveyor de rodillos'
        )