# Problema de los Misioneros y Caníbales: Búsqueda No Informada

Repositorio académico correspondiente a la evaluación empírica y modelado matemático del problema clásico de los Misioneros y Caníbales mediante estrategias de búsqueda ciega: **Búsqueda en Anchura (BFS)** y **Búsqueda en Profundidad (DFS)**.

* **Institución:** Escuela Politécnica Nacional (EPN)
* **Facultad:** Facultad de Ingeniería de Sistemas
* **Asignatura:** Inteligencia Artificial, Periodo Académico 2026-B
* **Autor:** Ricardo Cisneros
* **Correo Institucional:** ricardo.cisneros@epn.edu.ec

---

## 1. Descripción del Problema

Tres misioneros y tres caníbales deben cruzar un río empleando un bote con capacidad máxima para dos personas. La restricción fundamental de seguridad establece que si en alguna de las dos orillas el número de caníbales supera al de misioneros, estos últimos serán devorados.

### Formulación Matemática

El problema se define como la tupla $\mathcal{P} = \langle \mathcal{S}, s_0, \mathcal{S}_G, \mathcal{A}, T, c \rangle$:

* **Representación de estados:** $s = (M_L, C_L, B_L)$, donde $M_L, C_L \in \{0, 1, 2, 3\}$ denotan la cantidad de misioneros y caníbales en la orilla izquierda, y $B_L \in \{0, 1\}$ indica la ubicación del bote ($1$ izquierda, $0$ derecha).
* **Estado inicial:** $s_0 = (3, 3, 1)$
* **Estado objetivo:** $\mathcal{S}_G = \{(0, 0, 0)\}$
* **Acciones admisibles:** $\mathcal{A} = \{(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)\}$ indicando tripulantes a bordo.
* **Modelo de transición:** Suma o resta vectorial según la orientación del bote, garantizando que el estado sucesor preserve la condición de supervivencia:
  $$(M_L = 0 \lor M_L \ge C_L) \land (M_R = 0 \lor M_R \ge C_R)$$
* **Costo uniforme:** $c(s, a, s') = 1$ por cada travesía de río.

---

## 2. Resultados del Benchmarking Empírico

El protocolo experimental ejecutó 10,000 repeticiones consecutivas mediante `time.perf_counter()` para aislar fluctuaciones del sistema operativo:

| Métrica de Rendimiento | BFS (Cola FIFO) | DFS (Pila LIFO) |
| :--- | :---: | :---: |
| **Nodos expandidos totales** | **15** | **12** |
| **Tiempo de ejecución en frío** | $3.95 \times 10^{-5}\text{ s}$ | $2.38 \times 10^{-5}\text{ s}$ |
| **Tiempo promedio (10k ejecuciones)** | $2.74 \times 10^{-5}\text{ s}$ | $2.32 \times 10^{-5}\text{ s}$ |
| **Longitud del camino (cruces)** | **11** | **11** |
| **Tamaño máximo de frontera** | 3 nodos | 4 nodos |
| **Garantía teórica de optimalidad** | Sí (costo unitario) | No (condicional a la topología) |

### Secuencia Óptima Encontrada (11 pasos)

$$\begin{aligned}
(3,3,1) &\xrightarrow{(0,2)} (3,1,0) \xrightarrow{(0,1)} (3,2,1) \xrightarrow{(0,2)} (3,0,0) \xrightarrow{(0,1)} (3,1,1) \\
&\xrightarrow{(2,0)} (1,1,0) \xrightarrow{(1,1)} (2,2,1) \xrightarrow{(2,0)} (0,2,0) \xrightarrow{(0,1)} (0,3,1) \\
&\xrightarrow{(0,2)} (0,1,0) \xrightarrow{(1,0)} (1,1,1) \xrightarrow{(1,1)} (0,0,0)
\end{aligned}$$

---

## 3. Conclusiones Principales

1. **¿Garantizó DFS el camino más corto?:** Teóricamente, DFS no es admisible y no garantiza caminos mínimos. Sin embargo, en este problema particular devolvió 11 pasos porque **el espacio de estados conexo posee exactamente 4 caminos simples de inicio a fin y todos tienen longitud 11**. La optimalidad observada responde al estricto cuello de botella central del grafo y no a una propiedad del algoritmo.
2. **Consumo de memoria:** BFS almacena simultáneamente la capa horizontal completa de la frontera, con complejidad espacial $O(b^d)$, mientras que DFS mantiene únicamente la trayectoria activa y hermanos pendientes con crecimiento lineal $O(b \cdot m)$.

---

## 4. Instrucciones de Ejecución

Clonar el repositorio y ejecutar el script principal:

```bash
git clone https://github.com/ricardeinzz/misioneros-canibales.git
cd misioneros-canibales
python misioneros_canibales.py
```

### Requisitos

* Python 3.10 o superior
* `matplotlib` (para la exportación de gráficos comparativos)

```bash
pip install matplotlib
```

---

## 5. Estructura del Repositorio

* `misioneros_canibales.py`: Código fuente en Python con la formulación formal del problema, los algoritmos BFS y DFS, la reconstrucción de la solución y el benchmarking estadístico.
* `README.md`: Documentación técnica y guía de ejecución.
