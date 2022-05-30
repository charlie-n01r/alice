# Alice
## Avance 1:
Se crearon los archivos de `alice_lex.py` & `alice_yacc.py`. El primero de estos contiene todos los **tokens** que utiliza el lenguaje y exporta el **lexer** con los tokens.

`alice_yacc.py` importa el lexer y los tokens, y contiene toda la **gramática formal** del lenguaje Alice. Así mismo, cuenta con un set de instrucciones para probar la gramática utilizando lectura de archivos para _parsear_ sus contenidos.

Ambos archivos cuentan con un manejo de errores en caso de detectar una palabra o gramática incorrectamente.

## Avance 2:
Se agregó a la parte léxica el token **main**, que se utiliza para un nuevo conjunto de gramáticas diseñadas para separar el _main_ o cuerpo del archivo, de las funciones externas y variables globales. Esto se creó con el fin de facilitar el manejo de _scopes_ al momento de guardar variables en la tabla de variables.

Se creó el archivo `structs.py`, el cual contiene las siguientes estructuras de datos:
  - **var_object**: Este objeto representa un "renglón" en la tabla de variables. Guarda el ID, el tipo de dato de la varible, el valor que contiene al momento (en caso de tener), el _scope_ de dicha variable, así como el tamaño de la misma, si se trata de un arreglo.
  - **var_table**: La tabla de variables. Esta clase solamente contiene una lista a la que se le irán añadiendo objetos del tipo `var_object` al momento de declararse una nueva variable.
  - **fun_object**: Este objeto representa una entrada en el directorio de funciones y contiene información similar a la de `var_object` excepto por el campo de "valor". Así mismo, este objeto irá almacenando IDs de variables dentro de dos diferentes atributos tipo _list_ que se definieron para la clase. `parameters` almacenará los parametros de la función, mientras que `variables` almacenará las variables locales de la misma. En caso de que una función no tenga alguna de las ya mencionadas categorías, se dejará la lista vacía.
  - **fun_dir**: El directorio de funciones. Similar en estructura a `var_table`, se utilizará para almacenar instancias de `fun_object`.
  - **quadruple**: Los cuádruplos de las operaciones. Clase que provee la estructura básica de un cúadruplo, almacenando la operación a realizar, el o los operandos involucrados, así como el lugar donde se almacenará el resultado de la operación. En el futuro esta clase se extenderá para las operaciones de saltos.
  - **stacks**: Clase que contiene todas las pilas que se utilizan para la compilación: La pila de operadores, la pila de símbolos u operandos, y la pila de saltos.

Se creó el archivo `compile.py`, el cual solamente contiene el código utilizado para pruebas que se contenía dentro de `alice_yacc.py`. Esto a manera de modularizar más los archivos y dejar la lógica de la gramática separada de procesos ajenos.

### _Bugs_ conocidos:
  1. A pesar de que la gramática no marca ningún _warning_ u error, el parseo de una gramática que contenga estatutos compuestos (if-then-else, iteraciones) toma demasiado tiempo en parsear correctamente.
  2. Ocurren problemas similares con estatutos que son llamadas de función, ya sean funciones reservadas como _print_ o funciones del tipo `id(params...)`.

## Avance 3:
Se reestructuró la gramática para arreglar los bugs encontrados en el 2do avance. Aparentemente no hay ningún nuevo bug en la gramática.

Se agregó un archivo llamado `sem_cube.py`, el cuál contiene el cubo semántico del lenguaje. Se agregó también el código para la generación de cuádruplos una vez que se pase el filtro del cubo semántico.

Dentro del archivo `alice_yacc.py` se empezaron a generar algunas reglas vacías que funcionan como puntos neurálgicos para las expresiones con **or**, así como los valores estáticos y las variables simples. En el siguiente avance se buscará completar éste código y generar los respectivos códigos para el resto de las reglas de las expresiones y la de asignación, así como el avance pertinente de la semana siguiente.

## Avance 3.5:
Se terminó de agregar los puntos neurálgicos de todos los estatutos lineales y expresiones. Se implementaron mensajes de error semánticos al momento de querer realizar operaciones con parejas inválidas de operandos.

Se modificó `structs.py` para agegar la lista de cúadruplos, se simplificó la creación de objetos tipo cuádruplo, se removió el atributo de _value_ para los renglones de la tabla de variables, y se creó un método de exportación de cuádruplos a formato _json_ para futuro uso en la máquina virtual.

Se modificó `compile.py` para facilitar su uso al momento de parsear archivos.
Se agregó una función a manera de _log_ para exportar información pertinente a un archivo, y así evitar llenar la terminal de mucha información.

### _Bugs_ conocidos:
  1. Al finalizar el parseo y generación de cuádruplos de una expresión, se queda en el stack de tipos y de operandos la última variable temporal creada, así como su respectivo tipo. Esto no ha afectado el parseo de ningún estatuto consiguiente, pero a la larga provoca que crezcan ambas pilas, vacíandose solamente al momento de finalizar la ejecución.

## Avance 4:
En `alice_yacc.py` se agregaron los puntos neurálgicos para lo estatutos no lineales **if-then-else**, **while**, **do while** y **for**. Así mismo, se optimizó la creación de cuádruplos y se agregó el campo de _Largos_ al log para poder confirmar si la pila de operandos tiene el mismo largo que la pila de tipos al final de la ejecución.

Se simplificó la manera en la que se maneja la declaración de modulos y se agregó una verificación semántica para los estatutos de retorno para evitar returns globales, en main o funciones void.

Se identificó el bug encontrado en el avance 3.5, el cual ocurría cuando una expresión como `x++;` o similares, se ponían como único elemento de un estatuto, causando que nunca fueran sacados de la tabla de operadores, y por consiguiente, tampoco sus tipos.

Se eliminó de memoria el espacio reservado para strings temporales debido a que el lenguaje realmente no realiza operaciones con strings, por lo que son innecesarios. El espacio que ocupaban se le asignó a los bools temporales para poder tener más evaluaciones de lógica booleana.

Se agregó la creación del cuádruplo "Goto, MAIN", el cual actualmente no tiene funcionalidad y se reemplazó el uso de IDs en cuádruplos por el uso de direcciones de memoria virtual. Así mismo se empezó a contabilizar la memoria de variables temporales y se agregó manejo de errores para los casos de _too many constants_ y _too many variables_ para todos los ambientes (locales, globales y temporales). Se incluyó también la lógica para meter modulos dentro del directorio de funciones y el comienzo del código para conservar los parámetros formales de una función declarada.

Finalmente, se cambió la manera en la que funciona la exportación por medio de JSON para incluir también la tabla de constantes y para hacer la lógica extendible en caso de que se necesite exportar más información para la máquina virtual.

## Avance 5:
Se agregaron los puntos neurálgicos y la lógica detrás del parseo de creación y llamada de módulos, así como la verificación semántica que implican las operaciones entre modulos, las asignaciones de modulos a variables y la lógica de los estatutos tipo `return`.

En `structs.py` se modificó la función _clear_ para limpiar solamente la memoria local entre definiciones de funciones, y así reutilizar espacios de memoria entre modulos. Se agregó también la creación de los cuádruplos relacionados con funciones y llamadas, y se creó la lógica que reemplaza el "Main" en el cuádruplo "Goto Main" por el índice del primer cuádruplo de la función main.

Por último, se agregó todo el manejo de errores relacionado con las operaciones mencionadas anteriormente, y se optimizó la lógica de un par de mensajes de error.

## Avance 5.5:
En `structs.py` se cambió el orden en el que se genera el archivo `vm_input.json`, al cual se le incluyó también los _starting points_ de la memoria para poder calcular el _offset_ en la máquina virtual.

Se creó el prototipo de la máquina virtual, construida utilizando el lenguaje de programación **Julia**. Este archivo lee el contenido de `vm_input.json`, que funciona básicamente como un _pseudo archivo OBJ_ parsea sus contenidos a un diccionario, y cicla a través de los cuádruplos para ejecutar sus instrucciones. Por el momento, sólamente puede procesar los estatutos de `print`, así como la parte de impresión de mensaje de los estatutos `input`.

Se creó también un archivo ejecutable llamado `alice`, el cuál sirve como reemplazo del archivo `compile.py`, pero con algunas funcionalidades extra. Este archivo está escrito en **bash** y se encarga de correr `alice_yacc.py` y posteriormente la máquina virtual `vm.jl`, así como el manejo de errores necesario para manejar situaciones en donde la compilación no haya sido exitosa.

Hay dos maneras de procesar un archivo al momento de correr `alice`:
  1. **Pasarle archivos como argumentos**:
  ```bash
  user@linux:~/alice$ ./alice test0.aaw test1.aaw
  ```
  Al utilizar este método, `alice` iterará sobre los archivos y los procesará uno por uno. En caso de que alguno tenga un error de compilación, se le notificará al usuario y se detendrá por completo el proceso de compilación de los demás archivos, en caso de haber.

  2. **Correr `alice` sin argumentos**:
  ```bash
  user@linux:~/alice$ ./alice
  ```
  Al usar este método, el usuario entrará a una pequeña interfaz que le solicitará el nombre de un archivo que quiera parsear. Si se le inserta la frase `quit()` se terminará la ejecución del compilador, si se le provee el nombre de un archivo, lo intenterá compilar. Posteriormente, se le preguntará al ususario si desea compilar otro archivo, si el ususario inserta **n**, la ejecución de `alice` terminará, de lo contrario, se le volverá a solicitar al ususario el nombre de un archivo.

## Avance 6:
En `sem_cube.py` se corrigió un error que provocaba que el resultado de una división de enteros diera como resultado un número entero en vez de un número float. En `alice_yacc.py` se arreglaron algunos cuádruplos mal diseñados que se generaban al procesar un ciclo _for_, así como los estatutos `x++` o `x--`.\
Se cambió el nombre del archivo JSON a `obj.json` para mejor reflejar su función. Para reflejar este cambio se ajustó también el nombre dentro del ejecutable `alice`, así como la máquina virtual.

Se creó el archivo `virtual_memory.jl` el cual contiene las clases, estructuras de datos y funciones que le proveen memoria a la máquina virtual, almacenada ahora en el archivo `virtual_machine.jl`:
  - **Clases**:
    - **Persistent** es la memoria donde se almacenan las variables no temporales y las constantes. Como atributos tiene 3 arreglos de tipos _int64_, _float64_ y _string_.
    - **Temporary** sirve para almacenar las variables temporales. Ésta clase cuenta con un arreglo tipo _bool_ en su tercer atributo.
    - **Memory** es un tipo abstracto que es generalizado por Persistent y Temporary y sirve como abstracción sobre la que pueden operar las funciones de memoria.
    - **GlobalMem** es una estructura que representa a la memoria global, y está conformada de 2 memorias persistentes: las variables globales y las constantes.
    - **MemoryObj** representa la memoria local, y cuenta con una memoria persistente y una temporal.
  - **Funciones**:
    - **getMemory** retorna el atributo de memoria donde se buscará o almacenará un valor en base a un caractér que recibe como parámetro, así como el objeto de memoria donde buscará.
    - **fetch** retorna el valor dentro de un arreglo de memoria en base a un objeto de memoria recibido, la dirección en formato _uint16_ y el caractér con el que llamará a getMemory.
    - **store** se encarga de guardar valores basado en la misma información que recibe fetch, mas el valor que guardará, el cual es de tipo _any_. Si es necesario crear mas casillas para guardar el valor, las irá llenando con _nothing_ hasta poder meter el valor, de lo contrario, lo meterá en la casilla que se le solicitó con la address.
  - **Auxiliares**
    - **ranges** es un arreglo que cuenta con rangos numéricos que representa los rangos de memoria, lo cual ayuda a poder saber que tipo de memoria llamar al momento de hacer un fetch o store.
    - **operators** es un arreglo que contiene en formato _string_ todos los operadores que soporta el lenguaje Alice.

La máquina virtual en `virtual_machine.jl` actualmente puede soportar operaciones aritméticas, operaciones lógicas, prints, inputs del usuario, estatutos condicionales y ciclos. Así mismo, maneja errores semánticos como división entre 0 y generación de números imaginarios.

### ToDo:
  1. Agregar soporte en la máquina virtual de funciones.
  2. Agregar soporte de arreglos.
  3. Agregar soporte de funciones estadísticas.
  4. (Opcional) añadir más funciones estadísticas, si hay tiempo.

## Avance 6.5:
En `alice_yacc.py` se realizaron ajustes al código para poder generar funciones recursivas, generando cuádruplos completos que se pasarán a la máquina virtual.

En `structs.py` se removieron los rangos de memoria base que se enviaban en el `obj.json` para la máquina virtual debido a que ésta ya cuenta con los rangos dentro del archivo `virtual_memory.jl`.

En `virtual_machine.jl` se agregó soporte completo para las funciones, generando nueva memoria al momento de recibir una llamada, y separando el tamaño del espacio que ocupará de acuerdo con el cuádruplo _ARE_. Se han probado exitosamente casos con llamadas a funciones externas, incluyendo un archivo que recursivamente retorna el factorial de un número.

### ToDo:
  1. Agregar soporte de arreglos.
  2. Agregar soporte de funciones estadísticas.
  3. (Opcional) añadir más funciones estadísticas, si hay tiempo.

### _Bugs_ conocidos:
  1. Al intentar generar el "n" número fibonacci utilizando una función recursiva el programa retorna un resultado incorrecto. Los cuádruplos generados no son el problema, por lo que lo más seguro es que el error se encuentre dentro de la máquina virtual.

## Avance 7:
En `structs.py` se generó un nuevo rango de memoria de tipo _pointer_, el cual se usará para accesar la memoria al momento de realizar una indexación adentro de un arreglo. Así mismo, se incluyó una tabla de dimensiones para llevar el control de la dimensión actual y en qué variable se está indexando actualmente.

En `alice_yacc.py` se generaron los puntos neurálgicos para los arreglos unidimensionales, así como la evaluación semántica al momento de la creación e indexación en dichos arreglos, cuidando que no generen un arreglo con un número menor a 1 y que los índices sean de tipo entero.

Se arregló también el bug que provocaba que varias llamadas a función sobreescribieran el valor de la llamada anterior, como se observaba durante la secuencia fibonacci, creando una asignación a una variable temporal del resultado de una llamada a una función con valor de retorno.

En la máquina virtual se hicieron los cambios para soportar el nuevo tipo de dato pointer, mas aún no sea ha generado la lógica para respaldar el funcionamiento completo de los arrelos.

### ToDo:
  1. Agregar soporte de arreglos en máquina virtual.
  2. Agregar soporte de matrices.
  3. Agregar soporte de funciones estadísticas.

## Avance 8:
En `virtual_machine.jl` se generaron las verificaciones semánticas y el código intermedio para los arreglos y los datos de tipo _pointer_.

En `alice_yacc.py` se agregó el punto neurálgico para las funciones estadísticas, incluyendo una nueva función como extra del alcance del proyecto llamada **sum**. A continuación se describirá el comportamiento de las funciones soportadas:
    - **size(list)**: retorna un valor de tipo entero que corresponde al largo del arreglo proveído.
    - **mean(list)**: calcula el promedio de los valores contenidos en el arreglo que recibe como parámetro y retorna un valor de tipo _float_.
    - **median(list)**: calcula la mediana de los valores contenidos en el arreglo que recibe y retorna un valor de tipo _float_.
    - **mode(list)**: retorna la moda de los valores contenidos en el arreglo recibido como parámtro de la función, la cual puede ser _int_ o _float_ dependiendo del tipo del parámetro.
    - **variance(list)**: calcula la varianza de los valores contenidos en el arreglo que recibe y retorna un valor de tipo _float_.
    - **std(list)**: calcula la desviación estándar de los valores contenidos en el arreglo que recibe y retorna un valor de tipo _float_.
    - **sum(list)**: retorna la suma de los valores contenidos en el arreglo recibido como parámtro de la función, la cual puede ser _int_ o _float_ dependiendo del tipo del parámetro.

En `virtual_machine.jl` y `virtual_memory.jl` se creó el código intermedio para soportar funciones estadísticas, así como funciones y estructuras auxiliares necesarias para ejecutar dichas funciones.

Finalmente, se creó `datascience.aaw` para demostrar el funcionamiento de las funciones estadísticas implementadas hasta el momento.

### ToDo:
  1. Agregar soporte de matrices.
  2. Extender aún mas las funciones estadísticas.


## Avance 9:
En `alice_yacc.py` se agregó el punto neurálgico para utilizar matrices. Estas operaciones ya estaban implementadas en la máquina virtual, por lo que solamente se necesitó implementar la generación de cuádruplos para matrices.

Se actualizó estéticamente la ejecución del script `alice` para tener una interfaz más vistoza.

Se corrigieron las evaluaciones semánticas en expresiones que contenían uno o más valores de tipo pointer, ya que no generaban un valor de retorno de tipo booleano.
