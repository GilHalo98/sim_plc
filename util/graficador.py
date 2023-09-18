from graphviz import Graph
from .clases.lineas.linea import Linea
from .clases.zonas.tipos import TIPO_ZONA

def graficar_linea(
    linea: Linea,
    archivo_salida: str
) -> None:
    grafico = Graph(
        comment='Test',
        format='svg',
    )

    for nodo in linea.elementos:
        figura = 'box'
        if linea.elementos[nodo].tipo_zona is TIPO_ZONA.BRAZO_ROBOTICO:
            figura = 'circle'
        elif linea.elementos[nodo].tipo_zona is TIPO_ZONA.ESTACION:
            figura = 'square'
        elif linea.elementos[nodo].tipo_zona is TIPO_ZONA.TORNAMESA:
            figura = 'triangle'

        grafico.node(
            nodo,
            label=nodo,
            shape=figura
        )

        for conexion in linea.expandir(nodo):
            grafico.edge(
                nodo,
                conexion
            )

    grafico.node_attr['shape'] = 'circle'

    # Por ultimo renderiza el grafo en un archivo svg.
    # grafico.attr(overlap='false', compound='true')
    grafico.render(filename=archivo_salida)