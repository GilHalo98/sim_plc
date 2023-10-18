import sqlite3
import pathlib
import datetime
import multiprocessing


class Dbm():

    def __init__(
        self,
        nombre_db: str
    ) -> None:
        # Directorio de la base de datos temporal.
        self.__dir_db: pathlib.Path = pathlib.Path(nombre_db)

        self.__lock = multiprocessing.Lock()

        # Verificamos si ya existe la base de datos.
        if self.__dir_db.is_file():
            print('---> Cargando base de datos {}'.format(nombre_db), end='\t')
            # Instanciamos una conexión a la base de datos.
            self.__db_conexion = sqlite3.connect(self.__dir_db)
            print('[OK]\n')

        else:
            print('---> Creando base de datos {}'.format(nombre_db), end='\t')
            # Instanciamos una conexión a la base de datos.
            self.__db_conexion = sqlite3.connect(self.__dir_db)
            print('[OK]\n')

            # Creamos las tablas de la base de datos.
            self.__crear_tablas()

    def __crear_tablas(self) -> None:
        # Creamos un cursor.
        cursor = self.__db_conexion.cursor()

        cursor.execute('''PRAGMA journal_mode=WAL;''')

        print('---> Creando tabla: lineas', end='\t')
        cursor.execute('''
            CREATE TABLE lineas(
                id_linea INTEGER PRIMARY KEY AUTOINCREMENT,

                nombre_linea varchar(255) UNIQUE,

                fecha_registro datetime,
                fecha_modificacion datetime
            );
        ''')
        print('[OK]')

        print('---> Creando tabla: zonas', end='\t')
        cursor.execute('''
            CREATE TABLE zonas(
                id_zona INTEGER PRIMARY KEY AUTOINCREMENT,

                nombre_zona varchar(255),

                fecha_registro datetime,
                fecha_modificacion datetime,

                id_linea_vinculada varchar(255),

                FOREIGN KEY (id_linea_vinculada) REFERENCES zonas(nombre_linea)
            );
        ''')
        print('[OK]')

        print('---> Creando tabla: piezas', end='\t')
        cursor.execute('''
            CREATE TABLE piezas(
                data_matrix INTEGER NOT NULL UNIQUE PRIMARY KEY,
                tipo_pieza varchar(255),

                fecha_registro datetime,
                fecha_modificacion datetime,

                id_zona_vinculada int,

                FOREIGN KEY (id_zona_vinculada) REFERENCES zonas(id_zona)
            );
        ''')
        print('[OK]')

        print('---> Creando tabla: status', end='\t')
        cursor.execute('''
            CREATE TABLE status(
                id_status INTEGER PRIMARY KEY AUTOINCREMENT,

                tipo_status varchar(255),
                estado_status int,

                fecha_registro datetime,
                fecha_modificacion datetime,

                id_pieza_vinculada int,

                FOREIGN KEY (id_pieza_vinculada) REFERENCES piezas(data_matrix)
            );
        ''')
        print('[OK]\n')

        # Terminamos el cursor.
        cursor.close()

    def __push_linea(self, linea: 'Linea') -> None:
        '''
            Registra una linea en la base de datos.
        '''

        self.__lock.acquire()

        # Creamos un cursor.
        cursor = self.__db_conexion.cursor()

        # Instanciamos la fecha actual.
        hoy: datetime.datetime = datetime.datetime.today()

        # Instanciamos la transacción.
        transaccion: str = ''

        # Generamos el registro de la linea.
        print('---> Generando registro de linea: {}'.format(linea.id), end='\t')
        transaccion += '''
            INSERT OR IGNORE INTO lineas (nombre_linea, fecha_registro) VALUES ("{}", "{}");
        '''.format(linea.id, hoy.isoformat())
        print('[OK]')


        for zona in linea.elementos.values():
            print('---> Generando registro de zona: {}'.format(zona.id), end='\t')
            transaccion += '''
                INSERT OR IGNORE INTO zonas (nombre_zona, fecha_registro, id_linea_vinculada) VALUES ("{}", "{}", "{}");
            '''.format(zona.id, hoy.isoformat(), linea.id)
            print('[OK]')

        # Ejecutamos el registro de las zonas.
        print('---> Registrando zonas y linea', end='\t')
        cursor.executescript(transaccion)
        print('[OK]')

        # Terminamos el cursor.
        cursor.close()

        # Guardamos los cambios en la DB.
        print('---> Guardando cambios', end='\t')
        self.__db_conexion.commit()
        print('[OK]\n')
        self.__lock.release()

    def __push_pieza(self, id_linea: str, percepcion: dict) -> None:
        '''
            Registra o actualiza el estado de una
            pieza en la base de datos.
        '''

        self.__lock.acquire()

        # Creamos un cursor.
        cursor = self.__db_conexion.cursor()

        # Instanciamos la fecha actual.
        hoy: datetime.datetime = datetime.datetime.today()

        # Instanciamos la transacción.
        transaccion: str = ''

        for nombre_zona, pieza in zip(percepcion.keys(), percepcion.values()):
            # Consultamos el id de la zona registrada en la base de datos.
            id_zona: int = cursor.execute('''
                SELECT id_zona FROM zonas WHERE nombre_zona IS "{}" AND id_linea_vinculada IS "{}";
            '''.format(nombre_zona, id_linea)).fetchone()[0]

            # Registramos la pieza.
            transaccion += '''
                INSERT OR IGNORE INTO piezas (data_matrix, tipo_pieza, fecha_registro, id_zona_vinculada) VALUES ("{}", "{}", "{}", "{}");
                UPDATE piezas SET id_zona_vinculada = "{}", fecha_modificacion = "{}" WHERE data_matrix IS "{}";
            '''.format(
                pieza.data_matrix,
                pieza.tipo_pieza,
                hoy.isoformat(),
                id_zona,
                id_zona,
                hoy.isoformat(),
                pieza.data_matrix
            )

            for tipo_status, estado_status in zip(pieza.status.keys(), pieza.status.values()):
                # Registramos la pieza.
                transaccion += '''
                    INSERT OR IGNORE INTO status (tipo_status, estado_status, fecha_registro, id_pieza_vinculada) VALUES ("{}", "{}", "{}", "{}");
                    UPDATE status SET estado_status = "{}", fecha_modificacion = "{}" WHERE id_pieza_vinculada IS "{}" AND tipo_status IS "{}";
                '''.format(
                    tipo_status,
                    estado_status,
                    hoy.isoformat(),
                    pieza.data_matrix,

                    estado_status,
                    hoy.isoformat(),
                    pieza.data_matrix,
                    tipo_status
                )

        '''
UPDATE status SET estado_status="perro" WHERE EXISTS (
	SELECT * FROM piezas WHERE data_matrix IS 2015
);
        '''

        print(transaccion)

        # Ejecutamos el registro de las zonas.
        cursor.executescript(transaccion)

        # Terminamos el cursor.
        cursor.close()

        # Guardamos los cambios en la DB.
        self.__db_conexion.commit()

        self.__lock.release()

    def registrar_linea(self, linea: 'Linea') -> None:
        print('---> Registrando linea {}'.format(linea.id))
        hilo_registrar_linea = multiprocessing.Process(
            target=self.__push_linea,
            args=[linea]
        )
        hilo_registrar_linea.start()

    def update_estado_piezas(self, id_linea: str, percepcion: dict) -> None:
        if len(percepcion) > 0:
            hilo_registrar_pieza = multiprocessing.Process(
                target=self.__push_pieza,
                args=[id_linea, percepcion]
            )
            hilo_registrar_pieza.start()
