import json
import datetime
import sqlite3
import requests
from pathlib import Path
from datetime import datetime
from multiprocessing import Process, Queue, Lock


class Dbm_API(Process):
    '''
    '''

    def __init__(
        self,
        uri_api: str
    ) -> None:
        # Inicializamos la clase padre.
        super().__init__(target=self.__update, daemon=True)

        # Instanciamos una cola de operaciones.
        self.__cola_operaciones: Queue = Queue()

        # Instanciamos un bloqueo de recursos.
        self.__bloqueo_recursos: Lock = Lock()

        # Direccion de la api.
        self.__uri_api: str = uri_api

    def __update(self) -> None:
        '''
            Ejecuta las operaciones pendientes a la api.
        '''

        # Indicamos que se ejecutara el proceso de transacciones.
        print('---> Ejecutando procesamiento de transacciones')

        # Mientras el proceso siga vivo.
        while True:
            # Bloqueamos la cola de transacciones.
            self.__bloqueo_recursos.acquire()

            # Operacion pendiente.
            operacion = None

            # Si la cola de transacciones no esta vacia.
            if not self.__cola_operaciones.empty():
                # Recuperamos la trsansaccion.
                operacion = self.__cola_operaciones.get()

            # Liberamos la cola de transacciones.
            self.__bloqueo_recursos.release()

            # Si hay una operacion pendiente, se ejecuta.
            if operacion != None:
                respuesta = operacion['request'](
                    operacion['endpoint'],
                    json=operacion['datos']
                )

                print('---> Operacion ejecutada: {}'.format(
                    datetime.today()
                ))

                print('\tStatus: {} | Codigo: {}'.format(
                    respuesta.status_code,
                    respuesta.content[0]
                ))

        print('---> Procesamiento de operaciones terminado')

    def registrar_lineas(self, *lineas) -> None:
        '''
        '''
        # Datos de las lineas y sus zonas a registrar.
        datos_lineas: list = list()

        for linea in lineas:
            registro_linea: dict = {
                'nombreLinea': linea.id,
                'descripcionLinea': linea.descripcion,
                'zonas': list()
            }

            for zona in linea.elementos.values():
                registro_linea['zonas'].append({
                    'nombreZona': '{}_{}'.format(linea.id, zona.id),
                    'descripcionZona': zona.descripcion
                })

            datos_lineas.append(registro_linea)


        requests.api.post(
            'http://127.0.0.1:3001/apiv0.1.0/plc/registrar/lineasZonas',
            json={
                'lineas': datos_lineas
            }
        )

    def registrar_tipos_piezas(self, *tipos) -> None:
        for tipo in tipos:
            requests.api.post(
                'http://127.0.0.1:3001/apiv0.1.0/tipoPieza/registrar',
                json={
                    'descripcionTipoPieza': tipo.name
                }
            )

    def registrar_estados_status(self, *tipos) -> None:
        for tipo in tipos:
            requests.api.post(
                'http://127.0.0.1:3001/apiv0.1.0/estadoStatus/registrar',
                json={
                    'nombreEstado': tipo.name
                }
            )

    def registrar_tipos_reportes(self, *tipos) -> None:
        for tipo in tipos:
            requests.api.post(
                'http://127.0.0.1:3001/apiv0.1.0/tipoReporte/registrar',
                json={
                    'descripcionTipoReporte': tipo.name
                }
            )

    def registrar_tipos_status(self, tiposStatus) -> None:
        for tipoStatus in tiposStatus:
            requests.api.post(
                'http://127.0.0.1:3001/apiv0.1.0/tipoStatus/registrar',
                json={
                    'descripcionTipoStatus': tipoStatus
                }
            )

    def iniciar_tracking(self, pieza, id_linea, id_zona) -> None:
        datos_pieza = {
            'dataMatrix': pieza.data_matrix,
            'tipoPieza': pieza.tipo_pieza.name,
            'zonaActual': '{}_{}'.format(id_linea, id_zona),
            'status': [[
                id_status, pieza.status[id_status].name
            ] for id_status in pieza.status]
        }

        # Bloqueamos la cola de transacciones.
        self.__bloqueo_recursos.acquire()

        # Agregamos la operacion a la cola de operaciones.
        self.__cola_operaciones.put({
            'request': requests.api.post,
            'endpoint': 'http://127.0.0.1:3001/apiv0.1.0/plc/iniciar/tracking',
            'datos': datos_pieza
        })

        # Liberamos la cola de transacciones.
        self.__bloqueo_recursos.release()

    def generar_reporte(
        self,
        descripcion: str,
        data_matrix_pieza: str,
        id_zona: str,
        tipo_reporte: str
    ) -> None:
        '''
        '''
        # Bloqueamos la cola de transacciones.
        self.__bloqueo_recursos.acquire()

        # Agregamos la operacion a la cola de operaciones.
        self.__cola_operaciones.put({
            'request': requests.api.post,
            'endpoint': 'http://127.0.0.1:3001/apiv0.1.0/plc/generar/reporte',
            'datos': {
                'descripcionReporte': descripcion,
                'dataMatrix': data_matrix_pieza,
                'nombreZona': id_zona,
                'descripcionTipoReporte': tipo_reporte
            }
        })

        # Liberamos la cola de transacciones.
        self.__bloqueo_recursos.release()

    def update_percepcion(
        self,
        id_linea: str,
        percepcion: dict
    ) -> None:
        '''
        '''
        piezas: list = list()

        for id_zona in percepcion:
            pieza = percepcion[id_zona]

            datos_pieza = {
                'dataMatrix': pieza.data_matrix,
                'tipoPieza': pieza.tipo_pieza.name,
                'zonaActual': '{}_{}'.format(id_linea, id_zona),
                'status': [[
                    id_status, pieza.status[id_status].name
                ] for id_status in pieza.status]
            }

            piezas.append(datos_pieza)

        # Bloqueamos la cola de transacciones.
        self.__bloqueo_recursos.acquire()

        # Agregamos la operacion a la cola de operaciones.
        self.__cola_operaciones.put({
            'request': requests.api.post,
            'endpoint': 'http://127.0.0.1:3001/apiv0.1.0/plc/actualizar/tracking',
            'datos': { 'piezas': piezas }
        })

        # Liberamos la cola de transacciones.
        self.__bloqueo_recursos.release()

    def update_piesas_removidas(
        self,
        lista_piezas_removidas: list[str]
    ) -> None:
        '''
        '''

        # Bloqueamos la cola de transacciones.
        self.__bloqueo_recursos.acquire()

        # Agregamos la operacion a la cola de operaciones.
        self.__cola_operaciones.put({
            'request': requests.api.post,
            'endpoint': 'http://127.0.0.1:3001/apiv0.1.0/plc/terminar/tracking',
            'datos': { 'dataMatrixPiezas': lista_piezas_removidas }
        })

        # Liberamos la cola de transacciones.
        self.__bloqueo_recursos.release()

class Dbm(Process):
    '''
    '''

    def __init__(
        self,
        nombre_db: str
    ) -> None:
        # Inicializamos la clase padre.
        super().__init__(target=self.__update, daemon=True)

        # Instanciamos una cola de transacciones.
        self.__cola_transacciones: Queue = Queue()

        # Instanciamos un bloqueo de recursos.
        self.__bloqueo_recursos: Lock = Lock()

        # Directorio de la base de datos temporal.
        self.__dir_db: Path = Path(nombre_db)

        # Verificamos si ya existe la base de datos.
        if self.__dir_db.is_file():
            print(
                '---> Cargando base de datos {}'.format(nombre_db),
                end='\t'
            )

            # Limpiamos las piezas vinculadas.
            self.__limpiar_piezas_vinculadas()

            # Instanciamos una conexión a la base de datos.
            self.__db_conexion = sqlite3.connect(self.__dir_db)

            print('[OK]')

        else:
            print(
                '---> Creando base de datos {}'.format(nombre_db),
                end='\t'
            )

            # Instanciamos una conexión a la base de datos.
            self.__db_conexion = sqlite3.connect(self.__dir_db)

            print('[OK]')

            # Creamos las tablas de la base de datos.
            self.__crear_tablas()        

    def __limpiar_piezas_vinculadas(self) -> None:
        '''
        '''

        # Agregamos una transacción para eliminar la vinculación de
        # zonas de las piezas.
        transaccion: str = 'UPDATE piezas SET id_zona_vinculada = NULL;'

        # Agregamos la transacción a la cola de transacciones.
        self.add_transaccion(transaccion)

    def __crear_tablas(self) -> None:
        '''
        '''

        print('---> Creando tablas ', end='\t')

        transaccion: str = '''
            PRAGMA journal_mode=WAL;
        '''

        transaccion += '''
            CREATE TABLE lineas(
                nombre_linea varchar(255) UNIQUE PRIMARY KEY,

                fecha_registro datetime,
                fecha_modificacion datetime
            );
        '''

        transaccion += '''
            CREATE TABLE zonas(
                id_zona INTEGER PRIMARY KEY AUTOINCREMENT,

                nombre_zona varchar(255),

                fecha_registro datetime,
                fecha_modificacion datetime,

                id_linea_vinculada varchar(255),

                FOREIGN KEY (id_linea_vinculada) REFERENCES zonas(nombre_linea)
            );
        '''

        transaccion += '''
            CREATE TABLE piezas(
                data_matrix varchar(255) NOT NULL UNIQUE PRIMARY KEY,
                tipo_pieza varchar(255),

                fecha_registro datetime,
                fecha_modificacion datetime,

                id_zona_vinculada int,

                FOREIGN KEY (id_zona_vinculada) REFERENCES zonas(id_zona)
            );
        '''

        transaccion += '''
            CREATE TABLE status(
                id_status varchar(255) PRIMARY KEY,

                tipo_status varchar(255),
                estado_status int,

                fecha_registro datetime,
                fecha_modificacion datetime,

                id_pieza_vinculada varchar(255),

                FOREIGN KEY (id_pieza_vinculada) REFERENCES piezas(data_matrix)
            );
        '''

        # Creamos un cursor.
        cursor = self.__db_conexion.cursor()

        # Ejecutamos la transaccion.
        cursor.executescript(transaccion)

        # Terminamos el cursor.
        cursor.close()

        # Guardamos los cambios.
        self.__db_conexion.commit()

        print('[OK]')

    def __update(self) -> None:
        '''
            Ejecuta las transacciones a la base de datos.
        '''

        # Indicamos que se ejecutara el proceso de transacciones.
        print('---> Ejecutando procesamiento de transacciones')

        # Mientras el proceso siga vivo.
        while True:
            # Bloqueamos la cola de transacciones.
            self.__bloqueo_recursos.acquire()

            # Si la cola de transacciones no esta vacia.
            if not self.__cola_transacciones.empty():
                # Recuperamos la trsansaccion.
                transaccion = self.__cola_transacciones.get()

                print('\n---> Ejecutando transaccion: {}'.format(
                    transaccion
                ))

                # Creamos un cursor.
                cursor = self.__db_conexion.cursor()

                # Ejecutamos la transaccion.
                cursor.executescript(transaccion)

                # Terminamos el cursor.
                cursor.close()

                # Guardamos los cambios.
                self.__db_conexion.commit()

            # Liberamos la cola de transacciones.
            self.__bloqueo_recursos.release()

        print('---> Procesamiento de transacciones terminado')

    def registrar_lineas(self, *lineas) -> None:
        '''
        '''

        # Instanciamos la fecha actual.
        hoy: datetime = datetime.today()

        # Instancia de la transaccion.
        transaccion: str = ''

        for linea in lineas:
            transaccion += '''
                INSERT OR IGNORE INTO lineas (nombre_linea, fecha_registro) VALUES ("{}", "{}");
            '''.format(linea.id, hoy.isoformat())

            for zona in linea.elementos.values():
                transaccion += '''
                    INSERT OR IGNORE INTO zonas (nombre_zona, fecha_registro, id_linea_vinculada) VALUES ("{}", "{}", "{}");
                '''.format(
                    zona.id,
                    hoy.isoformat(),
                    linea.id
                )

        # Agreagamos la transaccion a la cola de transacciones.
        self.add_transaccion(transaccion)

    def update_percepcion(
        self,
        id_linea: str,
        percepcion: dict
    ) -> None:
        '''
        '''

        # Instanciamos la fecha actual.
        hoy: datetime = datetime.today()

        # Transaccion a realizar.
        transaccion: str = ''

        for id_zona, pieza in zip(
            percepcion.keys(),
            percepcion.values()
        ):
            # Por cada pieza en una zona, se agrega una transaccion
            # para registrar o actualizar la posicion de la pieza.
            transaccion += '''
                INSERT OR IGNORE INTO piezas (data_matrix, tipo_pieza, fecha_registro, id_zona_vinculada) VALUES ("{}", "{}", "{}", "{}");
                UPDATE OR IGNORE piezas SET id_zona_vinculada = "{}", fecha_modificacion = "{}" WHERE data_matrix IS "{}";
            '''.format(
                pieza.data_matrix,
                pieza.tipo_pieza,
                hoy.isoformat(),
                id_zona,
                id_zona,
                hoy.isoformat(),
                pieza.data_matrix
            )

            for tipo_status, estado_status in zip(
                pieza.status.keys(),
                pieza.status.values()
            ):
                # Por cada status posible de la pieza, se genera una
                # transacción para registrar el estado del status.
                transaccion += '''
                    UPDATE OR IGNORE status SET estado_status = "{}", fecha_modificacion = "{}" WHERE id_status IS "{}";
                    INSERT OR IGNORE INTO status (id_status, tipo_status, estado_status, fecha_registro, id_pieza_vinculada) VALUES ("{}", "{}", "{}", "{}", "{}");
                '''.format(
                    estado_status,
                    hoy.isoformat(),
                    '{}_{}'.format(pieza.data_matrix, tipo_status),
                    '{}_{}'.format(pieza.data_matrix, tipo_status),
                    tipo_status,
                    estado_status,
                    hoy.isoformat(),
                    pieza.data_matrix
                )

        # Agreagamos la transaccion a la cola de transacciones.
        self.add_transaccion(transaccion)

    def update_piesas_removidas(
        self,
        lista_piezas_removidas: list[str]
    ) -> None:
        '''
        '''

        # Instanciamos la fecha actual.
        hoy: datetime = datetime.today()

        # Transaccion a realizar.
        transaccion: str = ''

        for id_pieza_removida in lista_piezas_removidas:
            # Por cada pieza en la lista de piezas removidas
            # agregamos la transacción que desvincula la pieza con una
            # zona en una linea.
            transaccion += '''
                UPDATE OR IGNORE piezas set id_zona_vinculada = NULL, fecha_modificacion = "{}" WHERE data_matrix IS "{}";
            '''.format(
                hoy.isoformat(),
                id_pieza_removida
            )

        # Agreagamos la transaccion a la cola de transacciones.
        self.add_transaccion(transaccion)

    def add_transaccion(self, transaccion: str) -> None:
        '''
            Agrega una transaccion a la cola de transacciones.
        '''

        # Bloquea el Recurso a usar.
        self.__bloqueo_recursos.acquire()

        # Agrega la tranaccion a la cola.
        self.__cola_transacciones.put(transaccion)

        # Libera el recurso a usar.
        self.__bloqueo_recursos.release()