A continuación se describen las características que tendrá el lenguaje Alice, el cual está orientado a programación estadística y data science, con el enfoque a una sintaxis intuitiva desde un punto de vista matemático.

Debido a que el lenguaje está pensado como un lenguaje de scripting parecido a Python, la estructura de un archivo hecho en Alice no es estrictamente rígida. Es decir, cualquier línea de Alice puede ser una asignación, el inicio de una función, la generación de una gráfica, etc. Sin embargo, al principio del archivo debe de ponerse siempre “begin id :” para marcar el principio de este, así como “endprog” al final para marcar el final del mismo.

En su más mínima expresión, un archivo escrito en Alice se ve de la siguiente manera:
```matlab
begin ejemplo:
    statements;
endprog
```
## Expresiones y Operadores
### Operadores
El lenguaje Alice cuenta con la siguiente jeraquía de operadores:

| Precedencia | Operador                     | Descripción                               | Asociatividad |
|:------------|:-----------------------------|:------------------------------------------|:--------------|
| 1           | `x++`, `x--`                 | Incremento y decremento                   | Izq a Der 🡲  |
| 2           | `+x`, `-x`                   | Más y menos unario                        | Der a Izq 🡰  |
| 3           | `x^y`, `x*y`, `x/y`          | Exponenciación, Multiplicación y división | Izq a Der 🡲  |
| 4           | `x+y`, `x-y`                 | Suma y resta binaria                      | Izq a Der 🡲  |
| 5           | `x<y`, `x<=y`, `x>y`, `x>=y` | Operadores relacionales                   | Izq a Der 🡲  |
| 5           | `x==y`, `x¬=y`               | Operadores de igualdad                    | Izq a Der 🡲  |
| 6           | `x and y`                    | AND Lógico                                | Izq a Der 🡲  |
| 7           | `x or y`                     | OR Lógico                                 | Izq a Der 🡲  |
| 8           | `x <- y`                     | Asignación                                | Der a Izq 🡰  |

### Expresiones
En Alice la mayoría de las expresiones son formadas por un par de operandos con un operador en medio de ellos. Las únicas excepciones a esta regla son los operadores unarios. Los operadores de incremento y decremento, así como el operador de asignación son los únicos que tienen asociatividad por la derecha, todos los demás operadores tienen asociatividad por la izquierda.

## Declaraciones y Asignaciones
### Declaraciones
Existen 2 maneras de declarar una variable en Alice: _Declaración Simple_ y _Declaración con Asignación_, independientemente del tipo de declaración de variable, ambas empiezan con la palabra reservada `let`.

Una declaración simple es aquella donde se declaran una o más variables, especificando el nombre, seguido del tipo de variable que serán, pero sin asignarles un valor inicial. Es decir, se reserva simplemente el espacio de memoria que ocupará esa variable para futuras operaciones. Este tipo de declaración tiene la siguiente estructura:

```matlab
let L1::int[5];
let x::int, y::float;
```

Para crear una lista, es necesario siempre especificar el tamaño de la lista utilizando una constante entera entre corchetes después de especificar el nombre y el tipo de variable.

### Asignaciones
El operador de asignación en Alice es el símbolo `<-`. Alice es un lenguaje fuertemente tipado, es decir, **una vez que ha sido declarada una variable su tipo no cambiará hasta que ésta se destruya**. Existen 3 diferentes tipos de variable: `int`, `float` y `string`.

Para indexar en la lista y asignarle valor a un elemento en específico se utiliza la notación `list[pos]`, donde _pos_ es una expresión que retorne un número entero, una variable entera o una constante entera.

```matlab
x <- 2.3e-14;
L1[0] <- 0;
pi2 <- 6.283184;
```

## I/O
### Input
Para recibir información del usuario en Alice se utiliza la función de `input`. Esta función recibe un parámetro opcional en forma de una constante _string_ o una expresión para imprimir un mensaje que indique al usuario que está esperando un valor de entrada. Una vez recibido el valor, el compilador intentará parsear el dato recibido a uno de los tipos establecidos y asignarlo a una variable a través del operador de asignación `<-`.

```matlab
test <- input("Inserte una lista de números: ");
```
```
Inserte una lista de números: 1,2,3_
```

### Output
Para imprimir mensajes en la terminal se utiliza el comando `print`, función que recibe una o más expresiones. Implícitamente el comando convierte los datos recibidos en un _string_, concatenando los valores separados por comas con espacios y concatenando también un salto de línea (`\n`) al final.

```matlab
let x::int;
let y::float;
x <- 5;
y <- 10.0;
print(x, y);
print("Quince");
```
```
5 10.0
Quince
```

## Estructuras de control de flujo y bloques de código
### Condicionales
Una de las estructuras de flujo más básicas en un lenguaje de programación son los bloques _if-then-else_. Estas estructuras evalúan una expresión y, en base a la veracidad de la condición, entre o no al bloque `if`. De lo contrario, y en caso de existir un bloque `else`, entrará a éste último. Si no existe un bloque `else` y la evluación de la expresión es negativa, simplemente no entrará al bloque `if` y continuará con las instrucciones inmediatamente después de éste. Al final de todo el flujo de control se coloca la palabra reservada `end` para indicar que ha terminado el bloque.

```matlab
if 10 > 5 then:
  print(10);
end

let x:: int;
x <- input("Inserte un número: ");
if (x <= 10 and x > 0) then:
  print("El número está entre el 1 y el 10");
else:
  print("El número está fuera del rango 1-10");
end
```
```
10
Inserte un número: 11
El número está fuera del rango 1-10
```

### Ciclos _while_ y _do while_
Alice cuenta también con ciclos `while` y `do while`. Ambos esencialmente tienen la misma premisa: Evaluar una expresión y **mientras ésta sea verdadera** ejecutar las instrucciones contenidas en el bloque repetidamente hasta que la expresión se deje de cumplir y se salga del bloque, marcado también por la palabra reservada `end`. La única diferencia entre un ciclo que utiliza la palabra reservada `while` de uno que utiliza un `do while` es que éste último ejecutará los contenidos de su bloque **mínimo una vez y luego evaluará si la expresión es verdadera**.

```matlab
let x::int;
x <- 3;
while x > 0:
  print(x);
  x--;
end

do while (1 < 0):
  print("Si se ejecuta");
end
```
```
3
2
1
Si se ejecuta
```

### Ciclos _for_
Adicional a los ciclos anteriores, existe también el ciclo `for`. Este ciclo contiene atributos diferentes, separados por un punto y coma (`;`). El primer atributo es una declaración con asignación, o una asignación a secas, de la variable que se utilizará a lo largo del ciclo. En seguida está una expresión, similar a la que se utiliza en los ciclos _while_ y _do while_. El tercer atributo es una operación que permita cambiar el valor que recibió la asignación para acercar el ciclo a la condición de salida. Usualmente los ciclos for se utilizan para navegar a través de listas usando la variable inicializada como índice de la lista.

```matlab
let L::int[3];
let L <- [1, 2, 4.0];
let i::int;

for (i <- 2; i >= 0; i--):
  L[i] <- i;
end

for(i <- 0; i < 3; i++):
  print(L[x]);
end
```
```
0
1
2
```

## Funciones en Alice

### Funciones definidas por usuario
Alice le permite al usuario crear sus propias funciones con o sin valor de retorno. Las funciones definidas por usuario empiezan por la palabra reservada `module` seguida por el nombre que tendrá la función. SUsando el formato: `module name::type` se define el tipo de función de la que se tratará. `type` es uno de los 3 tipos que soporta Alice, sin embargo también existe el tipo `void` para las funciones que no retornan ningún tipo de valor. En la misma línea se deberá de poner entre paréntesis los atributos que recibirá la función, incluyendo el tipo de dichas variables.

Si la función no recibirá atributos, los paréntesis se dejan vacíos. Después de los atributos se indica que empieza el cuerpo de la función utilizando dos puntos `:` seguido del cuerpo de la función y al final la palabra reservada `end`. Si el tipo de la función no es `void` será necesario incluir la palabra reservada `return` seguido de una expresión que deberá de tener el mismo tipo que el valor de retorno de la función a la que pertenece antes del final de la función (`end`).

Las llamadas a función desde el cuerpo del programa tienen el formato `fun_name(attr1,..,attrn)`, donde `attr` son los atributos que se deberán mandar en la llamada a la función en caseo de que ésta los requiera. En el caso de una función que no tenga valor de retorno, esta llamada se colocará sola en la línea de código. En el caso de una función con valor de retorno, se aconseja utilizarla como elemento a asignar a una variable para guardar su valor.

```matlab
module nothing::void():
  print("This function only prints this text");
end

module five::int(number::int):
  if number ¬= 5:
    number <- 5;
  else:
    number <- number;
  return number;
end

nothing();
let x::int;
x <- five(1);
```
```
This function only prints this text
5
```

### Funciones estadísticas
Uno de los grupos de funciones más importantes en Alice son las funciones de [estadísticos descriptivos](https://en.wikipedia.org/wiki/Descriptive_statistics). Estas funciones trabajan con arreglos y sirven para resumir, así como describir características cuantitativas de un set de datos. En Alice están disponibles las siguientes:
  - Media (`mean`)
  - Mediana (`median`)
  - Moda (`mode`)
  - Varianza (`variance`)
  - Desviación Estándar (`std`)
  - Rango (`range`)
  - Tamaño (`size`)

Todas las anteriores funciones reciben un sólo parámetro, una expresión, y retornan siempre un resultado en tipo _float_, a excepción del rango y el tamaño. `range` siempre retorna una lista con los valores mínimos y máximos de un set de datos, mientras que `size` siempre retorna un entero.

Supongamos que se tiene una variable llamada `data` con los siguientes valores: `[9, 70, 93, 53, 92, 85, 75, 70, 68, 88, 76, 70, 77, 85, 82, 82, 80, 96, 100, 85]`
```matlab
let x::int;
let stats::float[5];

stats[0] <-mean(data);
stats[1] <-median(data);
stats[2] <-mode(data);
stats[3] <-variance(data);
stats[4] <- std(data);

for(x <- 0; x < size(results); x++):
  print(stats[x])
end

print(range(data));
```
```
76.8
81.0
70
377.6421052631579
19.433015856092894
[9, 100]
```

## Diagramas de sintaxis:

![Alice Language](https://user-images.githubusercontent.com/67932262/163838463-5f96f61e-75fe-4325-8a0f-53e065ca5333.png)
