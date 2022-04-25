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

## _Bugs_ conocidos:
  1. A pesar de que la gramática no marca ningún _warning_ u error, el parseo de una gramática que contenga estatutos compuestos (if-then-else, iteraciones) toma demasiado tiempo en parsear correctamente.
  2. Ocurren problemas similares con estatutos que son llamadas de función, ya sean funciones reservadas como _print_ o funciones del tipo `id(params...)`.
