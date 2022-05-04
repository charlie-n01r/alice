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
  - **quadruple**: Los cuadruplos de las operaciones. Clase que provee la estructura básica de un cúadruplo, almacenando la operación a realizar, el o los operandos involucrados, así como el lugar donde se almacenará el resultado de la operación. En el futuro esta clase se extenderá para las operaciones de saltos.
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
En `alice_yacc.py` se agregaron los puntos neurálgicos para lo estatutos no lineales **if-then-else**, **while**, **do while** y **for**. Así mismo, se optimizó la creación de cuadruplos y se agregó el campo de _Largos_ al log para poder confirmar si la pila de operandos tiene el mismo largo que la pila de tipos al final de la ejecución.

Se identificó el bug encontrado en el avance 3.5, el cual ocurría cuando una expresión como `x++;` o similares, se ponían como único elemento de un estatuto, causando que nunca fueran sacados de la tabla de operadores, y por consiguiente, tampoco sus tipos.

Se eliminó de memoria el espacio reservado para strings temporales debido a que el lenguaje realmente no realiza operaciones con strings, por lo que son innecesarios. El espacio que ocupaban se le asignó a los bools temporales para poder tener más evaluaciones de lógica booleana.
