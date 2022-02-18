# Informe Trabajo Final Modelo de Optimización 2

## Introducción

## Problema

## Desarrollo

### Primeras Observaciones

Luego de debatir varias ideas con el cliente; se terminó concluyendo que se ajustaba más un pequeño
framework, que este orientado hacia el dominio y terminología del `simplex` y toda la teoría que este
contiene, que un nuevo lenguaje implementado desde cero. El _DSL_ que necesita el cliente debe tener
las siguientes características:

- _Debe ser un lenguaje imperativo_: Al ser un framework, y no un nuevo lenguaje, el _DSL_ ya de inicio
  cuenta con todas las herramientas necesarias para cumplir con estas características provenientes del
  lenguaje base

- _El código resultante debe ser lo más cercano posible a la descripción teórica del algoritmo_: Para
  lo cual el desarrollo se apoya en algunas características especiales del lenguaje para simular,
  sistemas de ecuaciones, definiciones de funciones de cambios y pivoteos , etc ...

- _Debe tener la características de no ser imprescindible_: El fin del proyecto es, lograr un producto
  final que sirva de apoyo para el estudio y la evaluación de los contenidos relacionados con el
  algoritmos `simplex` en la carrera de ciencias de la computación. Debido al método evacuativo de
  la asignatura, la acumulación de créditos a lo largo del curso que puedan facilitar las evaluaciones
  finales, por tanto si el _DSL_ resultante formará parte de dichas evaluaciones los estudiantes con
  pocos o ningún crédito también deben poderse evaluar. Razón que refuerza la idea de un framework
  frente a un nuevo lenguaje, pues siempre se podría prescindir del framework e implementar los
  algoritmos en el lenguaje base

### Implementación

Apoyados en las consideraciones iniciales, se selecciono como lenguaje base para el desarrollo del
framework, al lenguaje **Python**, lenguaje imperativo, con el que los estudiantes de ciencia
de la computación tiene bastante contacto a lo largo de la carrera, además de contar con los
famosos "métodos mágicos" que brinda grandes facilidades para el desarrollo de dsl internos.
Además **Python** cuenta con la librería **numpy** que será de gran apoyo para el trabajo con
matrices, vectores y demás. El desarrollo de dividió de en varias fases

- _Formato_: en esta sección de desarrollo todas las herramientas que para lograr un dsl interno
  que brindara la sensación de estar definiendo un problema de optimización linea y su posterior
  transformación de la forma estándar, entrada requerida de los algoritmos `simplex`. Ejemplo:

  ```python
    pol.min_z = 2 * x[0] + 1 * x[1] + 3 * x[2] + 2 *x[3] +1* x[4]
    pol.s_a = (
         1 * x[0] + 1 * x[1] + 1 * x[2] + 1* x[3] == 9,
        -1 * x[0] + 1 * x[1] + 1 * x[2] + 1 * x[4] == 3
        )
  ```

- _Forma Explicita_: se definen varias estructuras para facilitar al desarrollador la definición,
  de forma matemática de los distintos componentes de los algoritmos `simplex`, como pueden
  ser _y0_ y _rj_

  ```python
    y0 = mo.inverse_matrix(B) * stand_eq.result_vector
    ztr = ctb * mo.inverse_matrix(B) * R
    rj = [(ctr[ir] - ztr[ir]) if index_in_base else 0 for index_in_base, _, ir in stand_eq.list_var_index_by(base) ]
  ```

- _Simplex_: se implementan las diferentes herramientas para facilitar tanto la definición de
  algoritmo `simplex` como su version de dos fases

  ```python
  while mo.check_optimal_condition(simplex_to_eq):
    aq = mo.find_input_column(simplex_to_eq)
    ap = mo.find_swap_column_to(aq, simplex_to_eq, _min = lambda yio, yiq: yiq/yio if yio > 0 else None)

    if ap is None: break # problema no acotado

    ypq = simplex_to_eq.Ax[ap][aq] # pivote
    simplex_to_eq = mo.swap_column_base(aq, ap, simplex_to_eq,
        formule= lambda i, j, yij, yiq, ypj: ypj/ypq if i == ap else yij - yiq * ypj / ypq)
  ```

- _Problema Dual_:
- _Cortes_:

### Documentación del DSL

El resultado final del trabaja es un framework con múltiples funciones y herramientas que facilitara
la definición y el procesamiento de un **Problema de Optimización Linea**, así como su resolución mediante
el algoritmo `simplex` y sus diferente interpretaciones. Dicho framework se documenta a continuación

El framework se conforma de un gran módulo de funciones estáticas, que el desarrollador debe importa:

```python
import simplex_framework as mo

```

La `format_componet` es la función inicial, esta tiene como resultado una tupla de dos elementos una
"lista infinita de variables" y un POL, el cual espera que se le asignen las propiedades min_z o
max_z y s_a haciendo uso de la "lista infinita de variables". El método `format_componet`siempre debe
acompañarse del método `get_stand_form` que dado un POL genera otro en la forma estándar, requisito
necesario para el algoritmo `simplex`. De la explotación de este método se obtiene la siguiente sintaxis:

```python
x, pol = mo.format_componet()
pol.min_z = 2 * x[0] + 1 * x[1] + 3 * x[2] + 2 *x[3] +1* x[4]
pol.s_a = (
       1 * x[0] + 1 * x[1] + 1 * x[2] + 1* x[3] == 9,
      -1 * x[0] + 1 * x[1] + 1 * x[2] + 1 * x[4] == 3
      )

stand_pol = mo.get_stand_form(pol)
```

Seguido de la definición del problema que se desea optimizar comienza los distintos pasos del algoritmo,
comenzando por la selección de la base de la matriz se restricciones. En este pasos comienzan las
bifurcación pues en dependencia de si la matriz presenta una base canónica o no, se pueden decidir
varias opciones en la resolución del ejercicio. Por tanto el framework aporta una lista de funciones
para cubrir todas las posibles decisiones del desarrollador.

```python
canonical_columns = mo.get_canonical_columns(pol) # retorna una lista de indices de las columnas canónicas
is_base = mo.is_base(canonical_columns, pol) # predicado afirmativo si las columnas de la lista son una base de Ax
base = mo.get_base(pol, canonical_columns) # completa una base de Ax que contenga los vectores de la lista
                                           # del segundo argumento, este es opcional y por default = []
pol_to_firts_fase, base = mo.complet_canonical_base(pol, canonical_columns)
# crea un nuevo problema al que se le agregan
# vectores canónicos que faltaban en el problema inicial
# además retorna la base canonica completada
```

Una vez seleccionada la base con la que se comenzará el algoritmo, independiente de la bifurcación
seleccionada, el siguiente pasos sería realizar las transformaciones necesarias para expresar el problema
de manera explicita respecto a la base seleccionada. En pos de ganar en expresividad y lenguaje matemático
se definió la interfaz `Operador`, al que se le modificaron los principales operadores aritméticos y que
internamente utilicé las operaciones que brinda `numpy` en el trabajo con matrices y vectores:

```python
ctb, ctr, B, R = mo.explicit_descompose(stand_eq, base)
y0 = mo.inverse_matrix(B) * stand_eq.result_vector
ztr = ctb * mo.inverse_matrix(B) * R

# el método list_var_index_by es un método de la clase LinealOptimizationProblem
# esta clase es la interface de entrada a todos los métodos antes expuestos
# el método es un iterador de 0 a la dimension del problema
# en cada paso resuelve una terna de
# 1- booleano que responde a si el indice pertenece a la base
# 2- indice de iteración
# 3- indice de iteración de los vectores que no pertenecen a la base
rj = [(ctr[ir] - ztr[ir]) if index_in_base else 0 for index_in_base, _, ir in stand_eq.list_var_index_by(base) ]
```

Una vez se tienen las herramientas para iniciar el algoritmo el framework ofrece las herramientas
para escribir el mismo lo más cerca posible a la propia definición, tomando como base la interface `Simplex`,
definida de la siguiente manera:

```python
class Simplex:
    def __init__(self, base, ctx, Ax, y0, rj) -> None:
        self.base = base
        self.ctx = ctx
        self.Ax = np.array(Ax)
        self.y0 = y0
        self.rj = rj
```

Apoyado en dicha interface y en varios métodos del framework se optiene la siguiente sintaxis :

```python
simplex_to_pol = mo.simplex_build(base, ctb, ctr, B, R, y0, rj) # instancia Simplex

while not mo.check_optimal_condition(simplex_to_pol):
  aq = mo.find_input_column(simplex_to_pol) # busca el menor rj negativo y retorna j
  # el method find_swap_column_to busca p fila de Ax
  # tal que la function _min sea mínima y distinta de None
  # siempre que exista aq
  ap = mo.find_swap_column_to(aq, simplex_to_pol, _min = lambda yio, yiq: yiq/yio if yio > 0 else None)

  if ap is None: break # problema no acotado

  ypq = simplex_to_eq.Ax[ap][aq] # pivote

  # realiza el cambio de base aplicando a lo largo de toda la tabla del simplex la función formule
  simplex_to_eq = mo.swap_column_base(aq, ap, simplex_to_eq,
      formule= lambda i, j, yij, yiq, ypj: ypj/ypq if i == ap else yij - yiq * ypj / ypq)
```

## Conclusiones
