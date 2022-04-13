# Alice
## Avance 1:
Se crearon los archivos de `alice_lex.py` & `alice_yacc.py`. El primero de estos contiene todos los **tokens** que utiliza el lenguaje y exporta el **lexer** con los tokens.

`alice_yacc.py` importa el lexer y los tokens, y contiene toda la **gramática formal** del lenguaje Alice. Así mismo, cuenta con un set de instrucciones para probar la gramática utilizando lectura de archivos para _parsear_ sus contenidos.

Ambos archivos cuentan con un manejo de errores en caso de detectar una palabra o gramática incorrectamente.
