"""

Qué hace este programa:
- Lee puntos (x,y) desde un CSV
- Grafica los puntos
- Calcula el Convex Hull (envolvente convexa)
- Dibuja el polígono resultante

Que hacer:
- Completar las funciones marcadas con TODO
- Probar con diferentes conjuntos de puntos

Requisitos:
- Python 3.x
- matplotlib

Instalación (si hace falta):
pip install matplotlib
"""

import csv
from typing import List, Tuple
import matplotlib.pyplot as plt

Point = Tuple[float, float]


def leer_puntos_csv(ruta_csv: str) -> List[Point]:
    """Lee un CSV con encabezados x,y y regresa una lista de tuplas (x,y)."""
    puntos: List[Point] = []
    with open(ruta_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            x = float(row["x"])
            y = float(row["y"])
            puntos.append((x, y))
    return puntos


def punto_mas_izquierdo(puntos: List[Point]) -> int:
    """
    Regresa el índice del punto más a la izquierda.
    En empate de x, escoger el de menor y (para hacerlo determinista).
    """
    idx = 0
    for i in range(1, len(puntos)):
        if puntos[i][0] < puntos[idx][0] or (puntos[i][0] == puntos[idx][0] and puntos[i][1] < puntos[idx][1]):
            idx = i
    return idx


def orientacion(a: Point, b: Point, c: Point) -> float:
    """
    TODO:
    Regresa el valor del producto cruz (cross product).

    Pista :
    cross = (b.x - a.x)*(c.y - a.y) - (b.y - a.y)*(c.x - a.x)

    Interpretación:
    - cross > 0  : giro antihorario (CCW)
    - cross < 0  : giro horario (CW)
    - cross == 0 : colineales
    """
    raise NotImplementedError("Completa la función orientacion(a, b, c)")


def distancia2(a: Point, b: Point) -> float:
    """Distancia al cuadrado (evita usar sqrt, no hace falta para comparar)."""
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return dx * dx + dy * dy


def convex_hull(puntos: List[Point]) -> List[Point]:
    """
    TODO:

    Idea general:
    1) Empieza en el punto más a la izquierda.
    2) En cada paso, elige el siguiente punto q tal que para cualquier otro punto r,
       el giro desde p hacia q sea el “más externo”.
    3) Repite hasta regresar al punto inicial.

    Nota:
    - Maneja colineales: si varios puntos quedan en la misma línea,
      quédate con el más lejano para que la envolvente quede “por fuera”.
    """
    if len(puntos) < 3:
        return puntos[:]  # no hay polígono

    hull: List[Point] = []
    start_idx = punto_mas_izquierdo(puntos)
    p_idx = start_idx

    while True:
        hull.append(puntos[p_idx])
        q_idx = (p_idx + 1) % len(puntos)

        for r_idx in range(len(puntos)):
            if r_idx == p_idx:
                continue

            # TODO:
            # 1) Calcula o = orientacion(p, q, r)
            # 2) Si r es “más externo” que q, entonces q = r
            # 3) Si son colineales, elige el más lejano a p
            #
            # Sugerencia de convención:
            # - Si tu orientacion devuelve >0 para CCW,
            #   normalmente querrás elegir el punto con giro CCW “más externo”.
            # Ajusta la condición según tu convención.
            pass

        p_idx = q_idx
        if p_idx == start_idx:
            break

    return hull


def dibujar(puntos: List[Point], hull: List[Point], titulo: str = "Convex Hull"):
    """Dibuja puntos y el polígono del hull."""
    xs = [p[0] for p in puntos]
    ys = [p[1] for p in puntos]

    plt.figure()
    plt.scatter(xs, ys)

    if len(hull) >= 2:
        hx = [p[0] for p in hull] + [hull[0][0]]
        hy = [p[1] for p in hull] + [hull[0][1]]
        plt.plot(hx, hy)

    plt.title(titulo)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.tight_layout()
    plt.show()


def main():
    # TODO: cambia la ruta al CSV que te indicó el profesor
    ruta = "coordenadas_768_puntos_0_1000.csv"

    puntos = leer_puntos_csv(ruta)
    hull = convex_hull_jarvis(puntos)

    print(f"Puntos: {len(puntos)}")
    print(f"Vértices del hull: {len(hull)}")

    dibujar(puntos, hull, titulo="Convex Hull (Jarvis March)")


if __name__ == "__main__":
    main()