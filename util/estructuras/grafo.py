class Grafo():
    def __init__(
        self,
        topologia: dict,
        elementos: dict
    ) -> None:
        '''
            Estructura de grafo.
        '''
        #  Topologia del grafo.
        self.__topologia: dict = topologia

        # Elementos del grafo almacenados en cada nodo.
        self.__elementos: dict = elementos

        # Nodos visitados, usado para recorridos o busqueda.
        self.__nodos_visitados: list = list()

    def __str__(self) -> None:
        pass

    @property
    def topologia(self) -> dict:
        return self.__topologia

    @property
    def elementos(self) -> dict:
        return self.__elementos

    @topologia.setter
    def topologia(self, topologia: dict) -> None:
        # Establecemos la topologia del grafo.
        self.__topologia = topologia

    @elementos.setter
    def elementos(self, elementos: dict) -> None:
        # Establecemos los elementos del grafo.
        self.__elementos = elementos

    def conexiones_en_nodo(self, id_elemento: str) -> int:
        # Indica cuantas conexiones tiene el nodo.
        return len(self.__topologia[id_elemento])

    def elemento_es_hoja(self, id_elemento: str) -> bool:
        # Indica si el nodo es hoja.
        return True if len(self.__topologia[id_elemento]) <= 0 else False

    def expandir(self, id_elemento: str) -> list:
        # Expande un nodo, reporta sus conexiones.
        return self.__topologia[id_elemento]

    def DFS(self, id_nodo: str, cola_visitas: list) -> str:
        '''
            Algoritmo de exploracion primero por profundidad (DFS)
        '''

        # Si el nodo no ha sido visitado.
        if id_nodo not in self.__nodos_visitados:
            # Agrega el nodo a los visitados.
            self.__nodos_visitados.append(id_nodo)

            # Si el nodo no es una hoja.
            if not self.elemento_es_hoja(id_nodo):
                # Expandimos la frontera.
                for id_conexion in self.expandir(id_nodo):
                    # Visitamos el nodo en la expancion y lo agregamos a los nodos visitados.
                    cola_visitas.append(self.DFS(id_conexion, cola_visitas))

            # Al terminar, retornamos el nodo expandido.
            return id_nodo

        # Retornamos el nodo.
        return id_nodo