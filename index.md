A continuación se describen las características que tendrá el lenguaje Alice, el cual está orientado a programación estadística y data science, con el enfoque a una sintaxis intuitiva desde un punto de vista matemático.

Debido a que el lenguaje está pensado como un lenguaje de scripting parecido a Python, la estructura de un archivo hecho en Alice no es estrictamente rígida. Es decir, cualquier línea de Alice puede ser una asignación, el inicio de una función, la generación de una gráfica, etc. Sin embargo, se le sugiere a los programadores que lo utilicen que sigan las estructuras convencionales de un archivo de código.

A continuación se explicará la sintaxis de estatutos en Alice, así como los tipos de datos que soporta y funciones internas que maneja el lenguaje.

## Expresiones y Operadores
### Operadores
El lenguaje Alice cuenta con la siguiente jeraquía de operadores:

| Precedencia | Operador                     | Descripción               | Asociatividad |
|:------------|:-----------------------------|:--------------------------|:--------------|
| 1           | `x^y`                        | Exponenciación            | Izq a Der 🡲  |
| 1           | `x++`, `x--`                 | Incremento y decremento   | Izq a Der 🡲  |
| 2           | `+x`, `-x`                   | Más y menos unario        | Der a Izq 🡰  |
| 3           | `x*y`, `x/y`                 | Multiplicación y división | Izq a Der 🡲  |
| 4           | `x+y`, `x-y`                 | Suma y resta binaria      | Izq a Der 🡲  |
| 5           | `x<y`, `x<=y`, `x>y`, `x>=y` | Operadores relacionales   | Izq a Der 🡲  |
| 5           | `x==y`, `x¬=y`               | Operadores de igualdad    | Izq a Der 🡲  |
| 6           | `x and y`                    | AND Lógico                | Izq a Der 🡲  |
| 7           | `x or y`                     | OR Lógico                 | Izq a Der 🡲  |
| 8           | `x <- y`                     | Asignación                | Der a Izq 🡰  |

### Expresiones
En Alice la mayoría de las expresiones son formadas por un par de operandos con un operador en medio de ellos. Las únicas excepciones a esta regla son los operadores unarios. Los operadores de incremento y decremento, así como el operador de asignación son los únicos que tienen asociatividad por la derecha, todos los demás operadores tienen asociatividad por la izquierda.

## Declaraciones y Asignaciones
### Declaraciones
Existen 2 maneras de declarar una variable en Alice: _Declaración Simple_ y _Declaración con Asignación_, independientemente del tipo de declaración de variable, ambas empiezan con la palabra reservada `let`.

Una declaración simple es aquella donde se declaran una o más variables, especificando el nombre, seguido del tipo de variable que serán, pero sin asignarles un valor inicial. Es decir, se reserva simplemente el espacio de memoria que ocupará esa variable para futuras operaciones. Este tipo de declaración tiene la siguiente estructura:

```matlab
let L1::list;
let x::int, y::float;
```

La declaración con asignación, como su nombre lo indica, es aquella donde, además de reservar el espacio de memoria y asignarle un tipo, se le asigna también un valor inicial a la variable. Una peculiaridad del lenguaje Alice es que cuando se declara una variable con asignación no es necesario especificar el tipo de valor de la variable, sino que Alice automáticamente detectará el tipo de variable que se le intenta asignar al id y le dará el tipo pertinente a la variable. Solamente se puede hacer una declaración con asignación por renglón.

```matlab
let L2 <- [1, 2, 3];
let zero <- 0;
let pi <- 3.1415;
```

### Asignaciones
Como se pudo observar brevemente en el ejemplo anterior, el operador de asignación en Alice es el símbolo `<-`. Alice es un lenguaje fuertemente tipado, por lo que, **sin importar como fue declarada la variable, una vez que tiene asociado un tipo, este no cambiará hasta que se destruya la variable en cuestión**. Existen 4 diferentes tipos de variable: `int`, `float`, `string` y `list`. Debido al enfoque orientado a análisis estadístico y data science de este lenguaje, las operaciones de _string_ (indexación, concatenación, etc.) no son soportadas.

El funcionamiento de las listas es similar a Python, donde no es necesario declarar un tamaño fijo para un arreglo y las listas pueden contener una variedad de diferentes tipos o solamente 1. Para indexar en la lista y asignarle valor a un elemento en específico se utiliza la notación `list[pos]`, donde _pos_ es una expresión que retorne un número entero, una variable entera o una constante entera.

```matlab
L1 <- [1, 1.0];
L1[0] <- 0;
pi2 <- 6.283184;
```

## I/O
### Input
Para recibir información del usuario en Alice se utiliza la función de `input`. Esta función recibe un parámetro opcional en forma de una constante _string_ o una variable _string_ para imprimir un mensaje que indique al usuario que está esperando un valor de entrada. Una vez recibido el valor, el compilador intentará parsear el dato recibido a uno de los tipos establecidos y asignarlo a una variable a través del operador de asignación `<-`.

Es importante comentar que para que un usuario introduzca como valor de entrada una lista completa el formato de entrada debe ser el siguiente: `val1,val2,val3,...,valn`. Es decir, un compendio de valores separados solamente por comas.

```matlab
test <- input("Inserte una lista de números: ");
```
```
Inserte una lista de números: 1,2,3_
```

### Output
Para imprimir mensajes en la terminal se utiliza el comando `print`, función que recibe uno o más parametros en la forma de una constante de cualquier tipo o el nombre de una variable, separados por comas.Implícitamente el comando convierte los datos recibidos en un _string_, concatenando los valores separados por comas con espacios y concatenando también un salto de línea (`\n`) al final.

```matlab
let X <- 5;
let L <- [10.0];
print(X, L[0]);
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
if(10 > 5):
  print(10);
end

let x <- input("Inserte un número: ");
if(x <= 10 and x > 0):
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
let x <- 3;
while(x > 0):
  print(x);
  x--;
end

do while(1 < 0):
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
let L <- [1, 2, 4.0];
let i::int;

for(i <- 2; i >= 0; i--):
  print(L[i]);
end

for(let x <- 0; x < 3; x++):
  L[i] <- L[i] + x;
  print(L[x]);
end
```
```
4.0
2
1
1
3
6.0
```

## Funciones en Alice
### Funciones de listas
Alice cuenta con 3 funciones que operan exclusivamente sobre listas: `insert`, `remove`, `size`.

La primera función recibe como primer parámetro el nombre de una variable tipo `list`, y como segundo parámetro un valor a insertar dentro de la lista, el cual puede ser el nombre de una variable o una constante de cualquier tipo. Al ejecutarse, se alterará la lista del primer parámetro, añadiendo el elemento del segundo parámetro **al final de la lista**.

La función `remove` recibe también 2 diferentes parámetros: El primer valor es el id de la lista a la que se le removerá un elemento y el segundo parámetro es la posición en el arreglo del elemento que se quiere remover. **Esta función reduce el temaño de la lista**.

Por último se encuentra la función `size`, la cuál recibe como único parámetro una lista o el nombre de una variable que contiene una lista y retorna como entero el tamaño de dicha lista.

```matlab
let L <- [1, 2, "tres"];
insert(L, 4);
insert(L, 5.0);
remove(L, 1):

for(let x <- 0; x < size(L); x++):
  print(L[x];
end
```
```
1
"tres"
4
5.0
```

### Funciones definidas por usuario
Alice le permite al usuario crear sus propias funciones con o sin valor de retorno. Las funciones definidas por usuario empiezan por la palabra reservada `module` seguida por el nombre que tendrá la función. Si la función no tendrá valor de retorno, no es necesario escribirlo, de lo contrario, será necesario declarar el tipo usando el formato: `module name::type` donde `type` es uno de los 4 tipos que soporta Alice. En la misma línea se deberá de poner entre paréntesis los atributos que recibirá la función, incluyendo el tipo de dichas variables.

Si la función no recibirá atributos, los paréntesis se dejan vacíos. Después de los atributos se indica que empieza el cuerpo de la función utilizando dos puntos `:` seguido del cuerpo de la función y al final la palabra reservada `end`. Si el tipo de la función fue especificado será necesario incluir la palabra reservada `return` seguido de una expresión que deberá de tener el mismo tipo que el valor de retorno de la función a la que pertenece antes del final de la función (`end`).

Las llamadas a función desde el cuerpo del programa tienen el formato `fun_name(attr1,..,attrn)`, donde `attr` son los atributos que se deberán mandar en la llamada a la función en caseo de que ésta los requiera. En el caso de una función `void`, es decir, una función que no tenga valor de retorno, esta llamada se colocará sola en la línea de código. En el caso de una función con valor de retorno, se aconseja utilizarla como elemento a asignar a una variable para guardar su valor.

```matlab
module nothing():
  print("This function only prints this text");
end

module five::int(number::int):
  if(number ¬= 5):
    number <- 5;
  else:
    number <- number;
  return number;
end


nothing();
let x <- five(1);
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

Todas las anteriores funciones reciben un sólo parámetro, una lista o una variable que contenga una lista, y retornan siempre un resultado en tipo _float_, a excepción del rango. Ésta última siempre retorna una lista con los valores mínimos y máximos de un set de datos.

```matlab
let data <- [9, 70, 93, 53, 92, 85, 75, 70, 68, 88, 76, 70, 77, 85, 82, 82, 80, 96, 100, 85];
let results::list;
insert(mean(data), results);
insert(median(data), results);
insert(mode(data), results);
insert(variance(data), results);
insert(std(data), results);
insert(range(data), results);

for(let x <- 0; x < size(results); x++):
  if(x == size(results) - 1):
    for(let y <-; y < 2; y++):
      print(results[x, y]);
  else:
    print(results[x]);
  end
end
```
```
76.8
81.0
70
377.6421052631579
19.433015856092894
9
100
```

### Funciones de graficación
Finalmente, como parte del kit de herramientas de ciencia de datos de Alice, se encuentran las funciones de graficación de datos. Estas funciones reciben de 2 a 3 parámetros, el último de cada función siendo una constante _string_ o una variable que tenga almacenado un _string_ que contenga la dirección y nombre que recibirá el archivo que contengrá la gráfica generada.

#### Funciones de una sola lista:
Estas funciones reciben, aparte del _string_ ya mencionado, una lista de _enteros_ o _floats_ que corresponderán a los puntos que se graficarán. Esta lista puede estar contenida dentro de una variable o ser una lista constante.
  - Histograma (`hist`)
  - Pie (`pie`)
  - Boxplot (`boxplot`)

#### Funciones de parejas X, Y:
Estas funciones reciben 2 pares de listas de _enteros_ o _floats_ que corresponderán a la parejas de puntos (x, y). La primera lista son los puntos X, mientras que la segunda lista son los puntos Y. Al igual que las funciones anteriores, estas pueden ser variables o listas constantes. **¡Cabe mencionar que ambas listas deben ser del mismo tamaño para poder generar una gráfica correcta!**
  - Línea 2D (`plot`)
  - Scatter plot (`scatter`)
  - Gráfica de Barras (`bar`)

```matlab
let Xs <- [0.56, 0.59, 0.68, 0.08, 0.28, 0.28, 0.57, 0.77, 0.07, 0.68];
let Ys <- [9, 70, 93, 53, 92, 85, 75, 70, 68, 88];

plot(Xs, Yx, "2dline.jpeg");
scatter(Xs, Ys, "scatter.png");
hist(Xs, "histogram.webp");
bar(Xs, Ys, "plots/bar.svg");
pie(Xs, "plots/pie.pdf");
boxplot(Xs, "plots/boxplot.png");
```
_El resultado de las anteriores operaciones generará los archivos pertinentes de acuerdo a los nombres recibidos como atributo._

## Diagramas de sintaxis:

![Alice Language](https://user-images.githubusercontent.com/67932262/162603147-a24db9b2-5a18-4b6b-b80f-00050a16d299.png)
