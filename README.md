# Juego-AgenteLogico
## Demogorgon Escape

Un videojuego lógico hecho en python

Pablo Gómez Martínez, 11 de enero 2023

## Introducción.
Antes de empezar a explicar cómo funciona, primero explicaremos el juego y sus reglas.
En este juego te encuentras atrapado en un sistema de cuevas, representado como una cuadrícula de 5x5. Cada cuadrícula es una habitación de la cueva en la que puede haber un agujero, el demogorgon, la salida de la cueva o nada. 
En cada turno puedes moverte en cualquier dirección, salvo en diagonal. Al caer en cualquiera de los 3 agujeros pierdes la partida. Al caer en el demogorgon, pierdes la partida, a no ser que, antes de entrar en su casilla, decidas disparar, en cuyo caso acabarás con él.
El objetivo del juego es acabar con el demogorgon y escapar de la cueva.
Para poder averiguar qué hay en cada casilla, el juego tiene un sistema de “sensaciones”. Si te encuentras en una casilla adyacente a un agujero sentirás una brisa, un cosquilleo si es un demogorgon o luz si es la salida.
Además, en los modos más fáciles, hay niveles de luz, de 0 a 3, donde la luz se intensifica cuanto más cerca de la salida estés, siendo el 3 para las casillas adyacentes.
Guiándote por la lógica, podrás ganar la partida.
Por último, el juego tiene dos versiones. En la primera, las sensaciones y el disparo son siempre certeros. En la segunda, no lo son. Es decir, en la versión probabilística hay probabilidades asociadas a sentir algo estando a su lado, a sentirlo aunque no sea así, y a fallar el disparo. También, cada versión tiene dos modos; uno en el cual un agente lógico te ayuda y otro en el cual tú mismo debes pensar todo.

## Menú principal.
Al iniciar el programa se nos presenta con el menú principal. Las opciones que nos permite no son muy variadas. Dificultades fácil, normal, difícil y dificultad demogorgon; además de la opción de salir del programa.
Las dos primeras dificultades corresponden al juego con certeza absoluta y las dos últimas al juego probabilístico. Las dificultades fácil y normal incluyen ayuda del programa. Nos devuelven las respuestas del agente lógico e imprimen los tableros de lógica automática.
Las otras dos no incluyen estas ayudas. En cada turno sólo tendremos la tabla de sensaciones, el tablero de juego, y nuestra propia cabeza.
La estética del menú principal también era importante ya que es la primera impresión que tenemos del juego. Por eso, tiene una estética algo macabra. con una imagen en caracteres del demogorgon.

## El tablero.
Para crear el tablero, utilizo un array de numpy ya que nos permite trabajar con vectores en todo el programa, lo cual es muy cómodo. 
Al inicio del juego, se colocan todos los obstáculos aleatoriamente, iniciando el jugador siempre en la esquina inferior izquierda.
No todos los tableros tienen solución. Por ejemplo, la salida puede encontrarse en una esquina rodeada de agujeros. Para dar siempre tableros posibles, antes de devolver el tablero se llama a una función de búsqueda. Esta función busca un camino desde el punto A hasta el punto B evitando cualquier obstáculo. Si encuentra caminos para llegar hasta la salida y hasta el demogorgon, el tablero es válido. Si no, se crea un nuevo tablero aleatorio y se repite el proceso.

## Representación de sensaciones.
Al pasar pr una casilla se imprimen las sensaciones correspondientes por pantalla. El jugador debería recordar las sensaciones de cada casilla, pero para facilitar las cosas en cada turno, a la izquierda del tablero principal, se imprime una tabla con las sensaciones que nos ha dado cada casilla. 
Además, en el tablero principal se indica con un número cada casilla por la que has estado, correspondiente al turno en el cual has pasado por primera vez. Estos números se relacionan directamente con la tabla de sensaciones.





## Mapa lógico.
En los modos fácil y normal cuentas con la ayuda de un agente lógico que, no sólo te recomienda cuál debería ser tu próximo movimiento, sino que genera un mapa lógico.
Este mapa es distinto para cada uno de los modos.
En el modo con certeza absoluta, el mapa lógico es similar al tablero de juego. Las casillas por las que has pasado se indican con un círculo. Se indican las casillas peligrosas con una exclamación “!” y las casillas en las que puede haber una salida con una interrodación “?”.
Además, si descubre la posición de algo lo indicará con una letra correspondiente. “A” para un agujero, “D” para el demogorgon y “S” para la salida.

En el modo probabilístico, nunca podemos tener certeza de que haya algo en una casilla adyacente, por lo que no se puede indicar la lógica de la misma manera. Para hacerlo esta vez, imprimimos un mapa algo más grande donde en cada casilla se marca la probabilidad de encontrar cada cosa. El diseño es feo y muy engorroso para el usuario y cambiarlo es uno de los primeros cambios de diseño que debería hacer en el futuro. Las probabilidades se aproximan a la decena a la hora de representarlas para mantenerlo más limpio, por eso las probabilidades que se muestran no son completamente exactas.

## Funcionamiento básico del modo con certeza.
Para el modo con certeza absoluta, lo primero que hace el programa es generar el mapa. Después, inicia el bucle de juego. En cada paso del bucle, el programa hace lo siguiente:
Obtiene qué sentimientos debe imprimir según la posición del jugador.
1. Rellena la base de conocimientos con los nuevos datos.
2. Procesa la nueva lógica.
3. Recomienda un próximo movimiento.
4. Obtiene el mapa, la tabla de sensaciones y el mapa lógico.
5. Imprime todos los datos y mapas de el turno por pantalla.
6. Pide al usuario que ingrese el próximo movimiento.

Los pasos 2, 3 y 4 sólo se hacen si se está jugando en modo fácil. En el caso del modo con certeza, las sensaciones se procesan en cada turno a partir del mapa y la posición del jugador. 
Al mover el jugador también se detecta si este ha perdido, ganado o acabado con el demogorgon.

## Lógica del modo con certeza.
En el modo con certeza, el agente lógico es una serie de funciones que trabajan sobre una estructura que funciona como base de conocimientos para determinar el contenido de las casillas del tablero.
La base de conocimientos es un diccionario cuyas claves son los tipos de obstáculos. “A” para agujeros, “D” para demogorgon y “S” para salida. Hay 3 posibilidades para los datos en cada clave y cada una significa algo distinto.
Una casilla seguido de “True” significa que sabe con certeza que el obstáculo indicado por la clave está en esa casilla.
Una casilla seguido de “False” significa que sabe con certeza que el obstáculo indicado por la clave NO está en esa casilla.
Varias casillas juntas significa que el obstáculo indicado por la clave puede estar en alguna de ellas. Es lo equivalente a un “OR”.
Cada vez que el jugador se mueve se añade la nueva información a la base de conocimientos. Sabemos que en la casilla a la que se ha movido el jugador no hay nada (a no ser que sea la salida o el demogorgon) y se añaden las cláusulas correspondientes. 
Después, se añaden las casillas adyacentes a las cláusulas “OR” si hemos sentido algo, o las indicamos como “False” en caso contrario. 
Por último, llamamos a la función de desarrollar la base de conocimientos. Esta función pasa por todas las cláusulas y hace resolución siempre que sea posible.

## Recomendación del próximo movimiento con certeza.
Con la lógica funcionando, recomendar un próximo movimiento es sencillo. El objetivo del agente es abrir el mapa de la forma más segura posible hasta encontrar al demogorgon y la salida, acabar con el demogorgon e ir a la salida.
Para cumplir este objetivo, el agente establece una serie de posiciones seguras, que son las posiciones por las que ya se ha pasado y sabemos que son seguras. Como moverse por las mismas posiciones no dará más información, busca posiciones sin peligro fuera de la frontera de explorados y establece cualquiera de ellas como objetivo.
En el caso de que todas las posiciones nuevas sean peligrosas, elige una aleatoriamente. Una posición peligrosa es aquella que se encuentre en una cláusula “OR” en la base de conocimientos (excepto si es de salida, ya que la salida es segura).
Para ganar, una vez el agente lógico averigua dónde se encuentra al demogorgon lo establece como objetivo, y al llegar a él recomienda, además de moverse, disparar.
Una vez eliminado, se dirige a la salida para ganar la partida.
Las casillas objetivo no siempre son adyacentes a la actual. Por eso, el agente recomendador tiene un algoritmo de búsqueda de caminos similar al que se utiliza para determinar si un tablero es posible. Este algoritmo crea el camino más corto desde la posición actual hasta el objetivo, pasando sólo por posiciones seguras.

## Funcionamiento básico del modo probabilístico.
Este modo funciona de una forma muy parecida pero con algunos cambios para que funcione con probabilidades. 
Al inicio del bucle y después de obtener el mapa, crea un mapa distinto que contendrá las sensaciones que nos devuelve cada casilla. Esta elección de diseño se debe a que, si sentimos de la misma forma que el modo normal, cada vez que pasemos por una celda nos dará un resultado diferente. Esto puede ser más realista, pero empeora la experiencia de juego ya que nos abre las puertas a una estrategia para hacer el juego más sencillo:
Esta estrategia consistiría en pasar por una casilla y volver atrás muchas veces seguidas. Cada vez nos daría unas sensaciones distintas pero, al apuntar cuántas veces sale la sensación, podríamos relacionarlo directamente con sus probabilidades asociadas y convertirlo en un juego con, básicamente, certeza absoluta.
Por eso, en este juego se hace un mapa de sensaciones en cada casilla, teniendo en cuenta sus probabilidades asociadas. El jugador se mueve por este mapa a la vez que por el mapa de juego y el programa imprime las sensaciones que nos dice esa casilla. Así, siempre obtendremos las mismas sensaciones todas las veces que pasemos por la casilla.
Otras diferencias con el modo normal se encuentran en el procesamiento de la base de conocimientos, explicada más tarde. Además, a la hora de disparar se analiza la probabilidad de acertar y no acaba con el demogorgon directamente.

## Lógica para el modo probabilístico.
En este modo la base de conocimientos es una clase en vez de un diccionario.
La estructura principal de esta clase es el mapa probabilístico. Es una array de numpy igual al mapa de juego, pero almacena en cada casilla las probabilidades asociadas a cada obstáculo. Cada casilla es un diccionario cuyas claves son los tipos de obstáculos y los datos son las probabilidades. También incluye un mapa con las posiciones ya exploradas.
Sus funciones más importantes son las funciones de hacer inferencia. Hay una por cada tipo de obstáculo. Estas funciones se llaman cada vez que nos movemos a una posición no explorada. Básicamente consisten en calcular un posterior con el teorema de Bayes, teniendo en cuenta las probabilidades previas y las probabilidades asociadas a cada suceso.
Después de calcular la nueva probabilidad, se actualiza la casilla. Pero, sl cambiar esta, la suma de las probabilidades en todas las casillas dejará de ser 1 (o 3 en el caso de los agujeros). Para arreglarlo, existe la función de ajuste de probabilidad. Esta función reparte la diferencia entre el prior y el posterior proporcionalmente en todo el tablero. Seguro que esto se puede solucionar de forma bayesiana, con redes bayesianas por ejemplo, pero no he logrado averiguar una manera mejor.
Finalmente, la función de certeza se llama cada vez que entramos en una casilla nueva. Esta función establece la probabilidad de que haya algo en esa casilla a 0 y vuelve a normalizar como antes. En caso de que la casilla sea la salida, establece la probabilidad de salida a 1 y en el resto de casillas a 0.

## Recomendación del próximo movimiento con probabilidad.
Similar a la función con certeza, esta función busca la casilla cercana más segura y se mueve a ella por un camino dentro de las posiciones exploradas.
Sin embargo, nunca tendremos certeza de que no haya nada en una casilla, por eso, se hace un ranking de seguridad en función de la suma de la probabilidad de demogorgon y agujero y elige la más segura dentro de lo posible.
Para ganar la partida hay que acabar con el demogorgon antes. Para ello, se establece un número completamente aleatorio que se puede cambiar como parte de los ajustes para el cual, si el valor de la probabilidad de demogorgon en una casilla es superior a este, estableceremos esta casilla como objetivo. Al llegar a ella, además de movernos recomendará disparar.
En el caso de que hayamos acabado con el demogorgon o bien no queden disparos el nuevo objetivo será la salida, si la conocemos, para acabar la partida, ya sea de forma victoriosa o neutral.

## Algunos detalles de diseño.
Un juego necesita una historia. Como no he visto Stranger Things, antes que meter la pata, decidí darle un pequeño giro.
En este juego, tú eres Spiderman y estás en una misión para acabar con el Demogorgon. Esto se aprovecha para explicar la mecánica del juego y las instrucciones. Además, en cada modo la historia cambia. En los modos con probabilidad, el Demogorgon y tú acabáis de tener una dura pelea y te ha dejado herido. Por eso, tu sentido arácnido no funciona del todo bien.
En los modos con asistencia, te has traído a la misión las gafas del señor Stark. La superinteligencia que tienen integrada es la que hace la lógica y te ayuda en la misión.
Otro detalle que se ha añadido, es la implementación del archivo “config.txt”. En este archivo se almacenan los valores de probabilidades y el jugador puede modificarlos a su gusto.

