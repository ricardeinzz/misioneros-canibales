"""
================================================================================
PROYECTO: EL PROBLEMA DE LOS MISIONEROS Y CANÍBALES
ASIGNATURA: INTELIGENCIA ARTIFICIAL (2026-B)
AUTOR: RICARDO CISNEROS
DESCRIPCIÓN:
Modelado matemático y empírico del problema clásico de los Misioneros y Caníbales.
Implementación de Búsqueda No Informada:
- Búsqueda en Anchura (BFS - Breadth-First Search) con Cola FIFO.
- Búsqueda en Profundidad (DFS - Depth-First Search) con Pila LIFO.
Evaluación de rendimiento (benchmarking) y extracción de métricas operativas.
================================================================================
"""

import time
import json
from collections import deque
import matplotlib.pyplot as plt

# ==============================================================================
# 1. FORMULACIÓN Y REGLAS DEL PROBLEMA
# ==============================================================================

ESTADO_INICIAL = (3, 3, 1)  # 3 misioneros, 3 caníbales, bote en orilla izquierda
ESTADO_OBJETIVO = (0, 0, 0)  # 0 misioneros, 0 caníbales, bote en orilla derecha

# Acciones admisibles: (misioneros_en_bote, canibales_en_bote)
# Capacidad del bote: mínimo 1, máximo 2 personas
ACCIONES = [
    (1, 0),  # Cruza 1 misionero
    (2, 0),  # Cruzan 2 misioneros
    (0, 1),  # Cruza 1 caníbal
    (0, 2),  # Cruzan 2 caníbales
    (1, 1),  # Cruza 1 misionero y 1 caníbal
]

def es_estado_valido(m_izq: int, c_izq: int) -> bool:
    """
    Verifica si una configuración de misioneros y caníbales cumple las
    restricciones de seguridad e invariancia del problema.
    
    Invariantes:
    1. Cantidades dentro del rango [0, 3].
    2. En la orilla izquierda: si hay misioneros, no pueden ser superados por caníbales.
    3. En la orilla derecha: si hay misioneros, no pueden ser superados por caníbales.
    """
    # Restricción de dominio físico
    if not (0 <= m_izq <= 3 and 0 <= c_izq <= 3):
        return False

    m_der = 3 - m_izq
    c_der = 3 - c_izq

    # Condición de supervivencia en la orilla izquierda
    if m_izq > 0 and m_izq < c_izq:
        return False

    # Condición de supervivencia en la orilla derecha
    if m_der > 0 and m_der < c_der:
        return False

    return True

def obtener_sucesores(estado: tuple) -> list:
    """
    Modelo de Transición T(s, a) -> s'.
    Dado un estado s = (m_izq, c_izq, bote_izq), genera todos los pares
    (sucesor, accion) que resultan de aplicar acciones legales.
    """
    m_izq, c_izq, bote_izq = estado
    sucesores = []

    for dm, dc in ACCIONES:
        if bote_izq == 1:
            # El bote se desplaza de Izquierda -> Derecha
            nuevo_m = m_izq - dm
            nuevo_c = c_izq - dc
            nuevo_bote = 0
        else:
            # El bote se desplaza de Derecha -> Izquierda
            nuevo_m = m_izq + dm
            nuevo_c = c_izq + dc
            nuevo_bote = 1

        if es_estado_valido(nuevo_m, nuevo_c):
            sucesores.append(((nuevo_m, nuevo_c, nuevo_bote), (dm, dc)))

    return sucesores

# ==============================================================================
# 2. ALGORITMOS DE BÚSQUEDA NO INFORMADA
# ==============================================================================

def reconstruir_camino(nodo_final, padres):
    """Reconstruye la secuencia de estados y acciones desde la raíz hasta la meta."""
    camino = []
    actual = nodo_final
    while actual is not None:
        padre, accion = padres[actual]
        camino.append((actual, accion))
        actual = padre
    camino.reverse()
    return camino

def bfs(estado_inicial=ESTADO_INICIAL, estado_objetivo=ESTADO_OBJETIVO):
    """
    Búsqueda en Anchura (Breadth-First Search)
    Estructura de frontera: Cola FIFO (collections.deque).
    Estrategia de exploración: Nivel por nivel.
    """
    t_inicio = time.perf_counter()
    
    # Frontera FIFO
    frontera = deque([estado_inicial])
    # Registro de visitados: estado -> (padre, accion)
    visitados = {estado_inicial: (None, None)}
    
    nodos_expandidos = 0
    tam_max_frontera = len(frontera)
    
    solucion_encontrada = False
    nodo_meta = None

    while frontera:
        if len(frontera) > tam_max_frontera:
            tam_max_frontera = len(frontera)

        actual = frontera.popleft()
        nodos_expandidos += 1

        if actual == estado_objetivo:
            solucion_encontrada = True
            nodo_meta = actual
            break

        for sucesor, accion in obtener_sucesores(actual):
            if sucesor not in visitados:
                visitados[sucesor] = (actual, accion)
                frontera.append(sucesor)

    t_fin = time.perf_counter()
    tiempo_total = t_fin - t_inicio

    camino = reconstruir_camino(nodo_meta, visitados) if solucion_encontrada else []

    return {
        "algoritmo": "BFS (Cola FIFO)",
        "exito": solucion_encontrada,
        "nodos_expandidos": nodos_expandidos,
        "tam_max_frontera": tam_max_frontera,
        "tiempo_segundos": tiempo_total,
        "longitud_camino": len(camino) - 1 if camino else 0,
        "camino": camino
    }

def dfs(estado_inicial=ESTADO_INICIAL, estado_objetivo=ESTADO_OBJETIVO):
    """
    Búsqueda en Profundidad (Depth-First Search)
    Estructura de frontera: Pila LIFO (list de Python).
    Estrategia de exploración: Hacia la máxima profundidad antes del retroceso.
    """
    t_inicio = time.perf_counter()
    
    # Frontera LIFO
    frontera = [estado_inicial]
    # Registro de visitados: estado -> (padre, accion)
    visitados = {estado_inicial: (None, None)}
    
    nodos_expandidos = 0
    tam_max_frontera = len(frontera)
    
    solucion_encontrada = False
    nodo_meta = None

    while frontera:
        if len(frontera) > tam_max_frontera:
            tam_max_frontera = len(frontera)

        actual = frontera.pop()
        nodos_expandidos += 1

        if actual == estado_objetivo:
            solucion_encontrada = True
            nodo_meta = actual
            break

        for sucesor, accion in obtener_sucesores(actual):
            if sucesor not in visitados:
                visitados[sucesor] = (actual, accion)
                frontera.append(sucesor)

    t_fin = time.perf_counter()
    tiempo_total = t_fin - t_inicio

    camino = reconstruir_camino(nodo_meta, visitados) if solucion_encontrada else []

    return {
        "algoritmo": "DFS (Pila LIFO)",
        "exito": solucion_encontrada,
        "nodos_expandidos": nodos_expandidos,
        "tam_max_frontera": tam_max_frontera,
        "tiempo_segundos": tiempo_total,
        "longitud_camino": len(camino) - 1 if camino else 0,
        "camino": camino
    }

# ==============================================================================
# 3. BENCHMARKING ESTADÍSTICO Y FORMATO
# ==============================================================================

def ejecutar_benchmark(num_repeticiones=10000):
    """
    Ejecuta ambos algoritmos repetidamente para mitigar el ruido del reloj del SO
    y obtener mediciones de tiempo de alta precisión y estabilidad estadística.
    """
    print(f"\n[+] Ejecutando Benchmarking Estadístico ({num_repeticiones:,} repeticiones)...")
    
    # Ejecución individual detallada
    resultado_bfs = bfs()
    resultado_dfs = dfs()

    # Muestreo de tiempos para BFS
    t0 = time.perf_counter()
    for _ in range(num_repeticiones):
        bfs()
    tiempo_promedio_bfs = (time.perf_counter() - t0) / num_repeticiones

    # Muestreo de tiempos para DFS
    t0 = time.perf_counter()
    for _ in range(num_repeticiones):
        dfs()
    tiempo_promedio_dfs = (time.perf_counter() - t0) / num_repeticiones

    resultado_bfs["tiempo_promedio_segundos"] = tiempo_promedio_bfs
    resultado_dfs["tiempo_promedio_segundos"] = tiempo_promedio_dfs

    return resultado_bfs, resultado_dfs

def imprimir_tabla_comparativa(res_bfs, res_dfs):
    """Imprime una tabla comparativa en formato legible por consola y Markdown."""
    ancho = 80
    print("\n" + "=" * ancho)
    print(" TABLA COMPARATIVA DE RENDIMIENTO EMPÍRICO (BFS vs DFS)".center(ancho))
    print("=" * ancho)
    print(f"{'Métrica':<38} | {'BFS (Cola FIFO)':<18} | {'DFS (Pila LIFO)':<18}")
    print("-" * ancho)
    print(f"{'Nodos expandidos totales':<38} | {res_bfs['nodos_expandidos']:<18} | {res_dfs['nodos_expandidos']:<18}")
    print(f"{'Tiempo de ejecución único (s)':<38} | {res_bfs['tiempo_segundos']:<18.6e} | {res_dfs['tiempo_segundos']:<18.6e}")
    print(f"{'Tiempo promedio (10k ejecuciones) (s)':<38} | {res_bfs['tiempo_promedio_segundos']:<18.6e} | {res_dfs['tiempo_promedio_segundos']:<18.6e}")
    print(f"{'Longitud del camino (acciones)':<38} | {res_bfs['longitud_camino']:<18} | {res_dfs['longitud_camino']:<18}")
    print(f"{'Tamaño máximo de la frontera':<38} | {res_bfs['tam_max_frontera']:<18} | {res_dfs['tam_max_frontera']:<18}")
    print(f"{'Garantía teórica de optimalidad':<38} | {'Sí (Costo unitario)':<18} | {'No (Depende de orden)':<18}")
    print("=" * ancho)

def imprimir_secuencia_camino(resultado):
    """Muestra la secuencia descriptiva de pasos de la solución encontrada."""
    print(f"\nSecuencia de Solución para {resultado['algoritmo']} ({resultado['longitud_camino']} pasos):")
    print("-" * 75)
    print(f"{'Paso':<5} | {'Estado Izq (M, C, B)':<22} | {'Acción del Bote':<20} | {'Orilla Der (M, C)'}")
    print("-" * 75)
    for i, (estado, accion) in enumerate(resultado["camino"]):
        m_i, c_i, b_i = estado
        m_d, c_d = 3 - m_i, 3 - c_i
        desc_bote = "Origen (Izq)" if b_i == 1 else "Destino (Der)"
        if accion is None:
            desc_acc = "Estado Inicial"
        else:
            dm, dc = accion
            desc_acc = f"Cruzan {dm}M, {dc}C ->"
        print(f"{i:<5} | ({m_i}, {c_i}, {b_i}) [{desc_bote:<12}] | {desc_acc:<20} | ({m_d}, {c_d})")
    print("-" * 75)

# ==============================================================================
# 4. GENERACIÓN DE FIGURAS PARA EL INFORME
# ==============================================================================

def generar_graficos(res_bfs, res_dfs, ruta_salida="grafico_comparativo.png"):
    """Genera un gráfico comparativo de barras de alta resolución para el informe en LaTeX."""
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.2), dpi=300)
    
    colores = ["#2b5c8f", "#d95f02"]
    algoritmos = ["BFS (FIFO)", "DFS (LIFO)"]

    # 1. Nodos expandidos
    axes[0].bar(algoritmos, [res_bfs["nodos_expandidos"], res_dfs["nodos_expandidos"]], color=colores, width=0.55)
    axes[0].set_title("Nodos Expandidos", fontsize=11, fontweight="bold")
    axes[0].set_ylabel("Cantidad de Nodos")
    for i, v in enumerate([res_bfs["nodos_expandidos"], res_dfs["nodos_expandidos"]]):
        axes[0].text(i, v + 0.3, str(v), ha="center", fontweight="bold")
    axes[0].grid(axis="y", linestyle="--", alpha=0.5)

    # 2. Tamaño Máximo de Frontera (Consumo de Memoria en Frontera)
    axes[1].bar(algoritmos, [res_bfs["tam_max_frontera"], res_dfs["tam_max_frontera"]], color=colores, width=0.55)
    axes[1].set_title("Tamaño Máx. de Frontera (Memoria)", fontsize=11, fontweight="bold")
    axes[1].set_ylabel("Nodos Concurrentes en Memoria")
    for i, v in enumerate([res_bfs["tam_max_frontera"], res_dfs["tam_max_frontera"]]):
        axes[1].text(i, v + 0.05, str(v), ha="center", fontweight="bold")
    axes[1].grid(axis="y", linestyle="--", alpha=0.5)

    # 3. Tiempo de Ejecución Promedio (microsegundos)
    tiempos_us = [res_bfs["tiempo_promedio_segundos"] * 1e6, res_dfs["tiempo_promedio_segundos"] * 1e6]
    axes[2].bar(algoritmos, tiempos_us, color=colores, width=0.55)
    axes[2].set_title("Tiempo Promedio (10k ejecuciones)", fontsize=11, fontweight="bold")
    axes[2].set_ylabel("Tiempo (μs)")
    for i, v in enumerate(tiempos_us):
        axes[2].text(i, v + 0.1, f"{v:.2f} μs", ha="center", fontweight="bold")
    axes[2].grid(axis="y", linestyle="--", alpha=0.5)

    plt.suptitle("Evaluación de Desempeño: Problema de los Misioneros y Caníbales", fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.savefig(ruta_salida, dpi=300)
    plt.close()
    print(f"[+] Gráfico comparativo exportado en: {ruta_salida}")

# ==============================================================================
# 5. PUNTO DE ENTRADA PRINCIPAL
# ==============================================================================

if __name__ == "__main__":
    res_bfs, res_dfs = ejecutar_benchmark(num_repeticiones=10000)
    imprimir_tabla_comparativa(res_bfs, res_dfs)
    imprimir_secuencia_camino(res_bfs)
    imprimir_secuencia_camino(res_dfs)
    generar_graficos(res_bfs, res_dfs, "misioneros_canibales/grafico_comparativo.png")
    
    # Exportar datos crudos a JSON para sincronización con el informe
    datos_exportacion = {
        "bfs": {
            "nodos_expandidos": res_bfs["nodos_expandidos"],
            "tam_max_frontera": res_bfs["tam_max_frontera"],
            "tiempo_segundos": res_bfs["tiempo_segundos"],
            "tiempo_promedio_segundos": res_bfs["tiempo_promedio_segundos"],
            "longitud_camino": res_bfs["longitud_camino"],
            "camino": [f"{s} vía {a}" for s, a in res_bfs["camino"]]
        },
        "dfs": {
            "nodos_expandidos": res_dfs["nodos_expandidos"],
            "tam_max_frontera": res_dfs["tam_max_frontera"],
            "tiempo_segundos": res_dfs["tiempo_segundos"],
            "tiempo_promedio_segundos": res_dfs["tiempo_promedio_segundos"],
            "longitud_camino": res_dfs["longitud_camino"],
            "camino": [f"{s} vía {a}" for s, a in res_dfs["camino"]]
        }
    }
    with open("misioneros_canibales/resultados_benchmark.json", "w", encoding="utf-8") as f:
        json.dump(datos_exportacion, f, indent=4, ensure_ascii=False)
    print("[+] Resultados de benchmark guardados en misioneros_canibales/resultados_benchmark.json")
