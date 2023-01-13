
#Importo librerías
import numpy as np
from copy import deepcopy

#Funcion para determinar si una posición existe dentro del tablero de juego
def pos_valida(pos):
            return pos[0] >= 0 and pos[0] < 5 and pos[1] >= 0 and pos[1] < 5

#Función para devolver un string con el mapa
def imprimir_mapa(mapa, n_salida):
    #━━ ┃ ┣ ┫ ┳ ┻ ╋ ┓ ┛ ┗ ┏
    #Imprime el mapa en pantalla
    mapa_imprimir = []
    mapa_imprimir.append("┏━━━┳━━━┳━━━┳━━━┳━━━┓\n")
    for i in range(5):
        for j in range(5):
            mapa_imprimir.append("┃")
            if mapa[i,j] == 4:
                #El jugador es una bola
                mapa_imprimir.append(" ● ")
            elif mapa[i,j] > 4:
                if mapa[i,j] == n_salida:
                    s = " S "
                else:
                    #Si hemos pasado por esa casilla se marca con el número correspondiente
                    s = " " + str(int(mapa[i,j])-4) + " "
                if len(s) == 4:
                    s = " " + str(int(mapa[i,j])-4)
                mapa_imprimir.append(s)
            else:
                mapa_imprimir.append("   ")
        mapa_imprimir.append("┃\n")
        if i < 4:
            mapa_imprimir.append("┣━━━╋━━━╋━━━╋━━━╋━━━┫\n")
    mapa_imprimir.append("┗━━━┻━━━┻━━━┻━━━┻━━━┛\n")
    return mapa_imprimir

#Función para rellenar el mapa lógico
def obtener_mapa_logico(kb):
    #Si la casilla marca true indico lo que hay en la casilla
    #Si la casilla marca false en las 3 indico que no hay nada
    #Si la casilla está contenida en una clausula con D o A indeterminada indico que hay que tener cuidado con "!"
    #Si la casilla está contenida en una clausula con S indeterminada indico que hay que puede estar con "?"
    mapa = np.zeros((5,5))
    #Relleno el mapa con los valores que tengo
    for i in range(5):
        for j in range(5):
            for conocimiento in kb:
                coords = list(conocimiento.values())[0]
                #Este conocimiento nos dice algo sobre enta casilla
                if (i,j) in coords:
                    if coords[1] == True:
                        #D es 1, A es 2, S es 3
                        if list(conocimiento.keys())[0] == "D":
                            mapa[i,j] = 1
                        elif list(conocimiento.keys())[0] == "A":
                            mapa[i,j] = 2
                        elif list(conocimiento.keys())[0] == "S":
                            mapa[i,j] = 3

                    elif coords[1] == False and mapa[i,j] != 4 and mapa[i,j] != 5 and mapa[i,j] != 1 and mapa[i,j] != 2 and mapa[i,j] != 3:
                        mapa[i,j] -= 1
                    elif  mapa[i,j] != 1 and mapa[i,j] != 2 and mapa[i,j] != 3:
                        #No hay certeza sobre lo que hay en esta casilla
                        if mapa[i,j] != 4: #El peligro tiene preferencia
                            mapa[i,j] = 4 if list(conocimiento.keys())[0] != "S" else 5 #4 is '!' and 5 is '?'
    return mapa

#Función para imprimir el mapa lógico
def imprimir_mapa_logico(kb):
    mapa = obtener_mapa_logico(kb)      
    mapa_imprimir = []
    mapa_imprimir.append("┏━━━┳━━━┳━━━┳━━━┳━━━┓\n")
    #Relleno cada casilla con su valor correspondiente
    for i in range(5):
        for j in range(5):
            mapa_imprimir.append("┃")
            if mapa[i,j] == -3:
                mapa_imprimir.append(" ● ")
            elif mapa[i,j] == 0:
                mapa_imprimir.append("   ")
            elif mapa[i,j] == 1:
                mapa_imprimir.append(" D ")
            elif mapa[i,j] == 2:
                mapa_imprimir.append(" A ")
            elif mapa[i,j] == 3:
                mapa_imprimir.append(" S ")
            else:
                s = "!" if mapa[i,j] == 4 else "?"
                mapa_imprimir.append(f" {s} ")
        mapa_imprimir.append("┃\n")
        if i < 4:
            mapa_imprimir.append("┣━━━╋━━━╋━━━╋━━━╋━━━┫\n")
    mapa_imprimir.append("┗━━━┻━━━┻━━━┻━━━┻━━━┛\n")
    return mapa_imprimir

#Función para imprimir la tabla de histórico de sensaciones en cada casilla
def imprimir_tabla_Sensaciones(mapa, sensaciones):
    mapa_imprimir = []
    max_casilla = 4
    casillas_numeradas = []
    #Obtengo las casillas para las que necesito devolver las sensaciones
    for i in range(5):
        for j in range(5):
            if mapa[i,j] > 3:
                casillas_numeradas.append(int(mapa[i,j]))
    casillas_numeradas.sort()
    max_casilla = casillas_numeradas[-1]
    casilla_jugador = max_casilla+1
    #Busco si hay un numero que falte en la lista de casillas numeradas
    #Si lo hay, el jugador está en una casilla que ya había visitado y que no quiero renombnrar
    for i in range(4, max_casilla):
        if i not in casillas_numeradas:
            casilla_jugador = i
            break
    pos_visitadas = []
    for i in range(5):
        for j in range(5):
            if mapa[i,j] > 4:
                pos_visitadas.append([(i,j), int(mapa[i,j])-4])
            if mapa[i,j] == 4:
                pos_visitadas.append([(i,j), casilla_jugador])
    #Oordena las posiciones visitadas por el número de la casilla
    pos_visitadas.sort(key=lambda x: x[1])
    pos_visitadas = [x[0] for x in pos_visitadas]
    #revertimos la lista para que se imprima de arriba a abajo
    pos_visitadas.reverse()
    mapa_imprimir.append("    ┏━━━━━┳━━━━━━━━━━┳━━━┓\n")
    mapa_imprimir.append("    ┃Brisa┃Cosquilleo┃Luz┃\n")
    mapa_imprimir.append("┏━━━╋━━━━━╋━━━━━━━━━━╋━━━┫\n")
    counter = 0
    
    #Imprimo las sensaciones de cada casilla
    for i in pos_visitadas:
        #Numero de casilla
        casilla = int(mapa[i]) if int(mapa[i]) != 4 else int(casilla_jugador)
        s = " " + str(int(casilla-4)) + " "
        counter += 1
        if len(s) == 4:
            s = " " + str(casilla-4)
        mapa_imprimir.append(f"┃{s}┃")
        #Brisa
        if sensaciones[i][0] == 1:
            mapa_imprimir.append("  X  ")
        else:
            mapa_imprimir.append("     ")
        mapa_imprimir.append("┃")
        #Cosquilleo
        if sensaciones[i][1] == 1:
            mapa_imprimir.append("    X     ")
        else:
            mapa_imprimir.append("          ")
        mapa_imprimir.append("┃")
        #Luz
        if sensaciones[i][2] != None:
            mapa_imprimir.append(f" {sensaciones[i][2]} ")
        else:
            mapa_imprimir.append(" 1 ")
        mapa_imprimir.append("┃\n")
        if counter < len(pos_visitadas):
            mapa_imprimir.append("┣━━━╋━━━━━╋━━━━━━━━━━╋━━━┫\n")
    mapa_imprimir.append("┗━━━┻━━━━━┻━━━━━━━━━━┻━━━┛\n")
    return mapa_imprimir

def mover_jugador(mapa, direccion, n_salida):
    #Mueve al jugador en la dirección indicada
    #Devuelve el mapa con el jugador movido
    #Si no se puede mover, devuelve el mismo mapa
    #Busco la posicion del jugador en el mapa:
    pos_jugador = (0,0)
    valores_casillas_pasadas = []
    for i in range(5):
        for j in range(5):
            if mapa[i,j] >= 4:
                valores_casillas_pasadas.append(int(mapa[i,j]))
            if mapa[i,j] == 4:
                pos_jugador = (i,j)
    pos_previa = pos_jugador
    #Guardamos el valor de la casilla y el valor máximo para indicar los conocimientos del jugador
    valor_pos_previa = None
    for i in range(4, max(valores_casillas_pasadas)):
        if i not in valores_casillas_pasadas:
            valor_pos_previa = i
            break
    if valor_pos_previa == None:
        valor_pos_previa = max(valores_casillas_pasadas)+1
    max_valor = 4
    for i in range(5):
        for j in range(5):
            if mapa[i,j] > max_valor:
                max_valor = mapa[i,j]

    #Movemos al jugador hacia el lado correspondiente
    if direccion == "derecha":
        pos_jugador = (pos_jugador[0],pos_jugador[1]+1)
    elif direccion == "izquierda":
        pos_jugador = (pos_jugador[0],pos_jugador[1]-1)
    elif direccion == "arriba":
        pos_jugador = (pos_jugador[0]-1,pos_jugador[1])
    elif direccion == "abajo":
        pos_jugador = (pos_jugador[0]+1,pos_jugador[1])
    #Comprobamos si la posición es válida
    if pos_valida(pos_jugador):
        #Comprobamos la situacion actual de la partida
        if mapa[pos_jugador] == n_salida:
            estado = "Win"
        elif mapa[pos_jugador] == 2:
            estado = "Lose"
        elif mapa[pos_jugador] == 1:
            estado = "Demogorgon"
        else:
            estado = None
        if mapa[pos_jugador] == n_salida:
            n_salida = 4
        
        #Un valor superior a 4 indica que el jugador ha estado en esa casilla y tienes conocimiento de ella
        elif mapa[pos_previa] == n_salida:
            n_salida = valor_pos_previa
        mapa[pos_jugador] = 4
        mapa[pos_previa] = valor_pos_previa
    else:
        return mapa, "Error"
    return mapa, estado, n_salida

#Función que maneja la entrada del usuario para manejar el turno del jugador
def obtener_nuevo_mapa(mapa, n_disparos, n_salida):
    ok = False
    while not ok:
        #Pido direccion de movimiento hasta que sea correcta
        print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("┃ Introduce la dirección de movimiento (U,D,L,R) y si desea disparar (S):   ┃")
        print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
        print(' O "SALIR" si desea abandonar el juego')
        entrada = input("   ->").upper().strip()
        entrada = entrada.split(" ")
        direccion = entrada[0]
        #Compruebo si el usuario quiere disparar
        if len(entrada) > 1:
            disparo = entrada[1]
        else:
            disparo = None
        if direccion == "U":
            mapa, estado, n_salida = mover_jugador(mapa, "arriba", n_salida)
        elif direccion == "D":
            mapa, estado, n_salida = mover_jugador(mapa, "abajo", n_salida)
        elif direccion == "L":
            mapa, estado, n_salida = mover_jugador(mapa, "izquierda", n_salida)
        elif direccion == "R":
            mapa, estado, n_salida = mover_jugador(mapa, "derecha", n_salida)
        elif direccion == "SALIR":
            estado = "Salir"
        else:
            print("Dirección incorrecta")
            continue
        if estado == "Error":
            print("No se puede mover en esa dirección")
            continue
        #Si el usuario dispara:
        if disparo == "S":
            #No quedan disparos
            if n_disparos == 0:
                print("No te quedan disparos")
                kill = None
                ok = True
            #Compruebo si se ha acabado con el demogorgon
            else:
                if estado == "Demogorgon":
                    kill = True
                    estado = None
                else:
                    kill = False
                ok = True
        else:
            kill = None
            ok = True
    return mapa, estado, kill, n_salida

def nivel_luz(mapa):
    #Devuelve el nivel de luz de la casilla en la que está el jugador
    pos_jugador = (0,0)
    for i in range(5):
        for j in range(5):
            if mapa[i,j] == 4:
                pos_jugador = (i,j)
    pos_salida = (0,0)
    for i in range(5):
        for j in range(5):
            if mapa[i,j] == 3:
                pos_salida = (i,j)
    #Distancia manhattan
    distancia = abs(pos_jugador[0]-pos_salida[0])+abs(pos_jugador[1]-pos_salida[1])
    if distancia > 8:
        return None
    elif distancia > 3:
        return "Hay una luz muy tenue"
    else:
        return "Hay algo de luz"

#Esta función devuelve la sensacion que proporciona esa casilla
def sensacion_casilla(casilla, mapa, n_salida):
    if casilla == 0:
        return nivel_luz(mapa)
    elif casilla == 1:
        return "Sientes un cosquilleo en la nuca"
    elif casilla == 2:
        return "Sientes una leve brisa"
    elif casilla == n_salida:
        return "Hay mucha luz"
    return None

def sentir(mapa, n_salida):
    #Devuelve una lista con las sensaciones que se sienten en ese casilla
    pos_jugador = (0,0)
    for i in range(5):
        for j in range(5):
            if mapa[i,j] == 4:
                pos_jugador = (i,j)
    arriba = (pos_jugador[0]-1,pos_jugador[1])
    abajo = (pos_jugador[0]+1,pos_jugador[1])
    izquierda = (pos_jugador[0],pos_jugador[1]-1)
    derecha = (pos_jugador[0],pos_jugador[1]+1)
    sensaciones = []
    if pos_valida(arriba):
        sensaciones.append(sensacion_casilla(mapa[arriba], mapa, n_salida))
    if pos_valida(abajo):
        sensaciones.append(sensacion_casilla(mapa[abajo], mapa, n_salida))
    if pos_valida(izquierda):
        sensaciones.append(sensacion_casilla(mapa[izquierda], mapa, n_salida))
    if pos_valida(derecha):
        sensaciones.append(sensacion_casilla(mapa[derecha], mapa, n_salida))
    sensaciones = list(set(sensaciones))
    #No puede haber más de un aviso de luz
    if "Hay una luz muy tenue" in sensaciones and "Hay algo de luz" in sensaciones:
        sensaciones.remove("Hay algo de luz")
    if "Hay una luz muy tenue" in sensaciones and "Hay mucha luz" in sensaciones:
        sensaciones.remove("Hay una luz muy tenue")
    if "Hay algo de luz" in sensaciones and "Hay mucha luz" in sensaciones:
        sensaciones.remove("Hay algo de luz")
    return sensaciones

#Pasa de una lista de sensaciones en strings a una lista de 3 elementos numéricos, más fáciles de trabajar
def sensaciones_simplificar(sensaciones):
    s = [None, None, None]
    for i in range(len(sensaciones)):
        if sensaciones[i] == "Sientes una leve brisa":
            s[0] = 1
        if sensaciones[i] == "Sientes un cosquilleo en la nuca":
            s[1] = 1
        if sensaciones[i] == "Hay una luz muy tenue":
            s[2] = 1
        elif sensaciones[i] == "Hay algo de luz":
            s[2] = 2
        elif sensaciones[i] == "Hay mucha luz":
            s[2] = 3
    return s

#Esta función concatena todos los mapas y los imprime juntos
def imprimir_estado_juego(sensaciones, mapa, mapa_logico):
    sensaciones = "".join(sensaciones)
    sensaciones = sensaciones.split("\n")[:-1]
    mapa = "".join(mapa)
    mapa = mapa.split("\n")
    mapa_logico = "".join(mapa_logico)
    mapa_logico = mapa_logico.split("\n")
    if len(sensaciones) < len(mapa):
        for i in range(len(sensaciones)-1, len(mapa)):
            sensaciones.append("                          ")
    for i in range(len(sensaciones)):
        s = sensaciones[i].replace("\n", "")
        s += " "*(5)
        try:
            s += mapa[i] + " "*(5) + mapa_logico[i]
        except:
            pass
        print(s)
    print("")

#Función que hace lógica a partir de la base de conocimientos
def desarrollar_base_conocimientos(kb):
    #La base de conocimientos es una lista de diccionarios
    #Cada diccionario es una parte de la información que sabes
    #Un diccionario puede ser de la forma:
    #{"D": (3,2), True} #Hay un demogorgon en la casilla (3,2)
    #{"D": (3,2), False} #No hay un demogorgon en la casilla (3,2)
    #{"D": (3,2), (2,1)} #Hay un demogorgon en la casilla (3,2) o en la casilla (2,1)
    #Tomamos la luz solo cuando el valor de luz es 3

    #Todas las simplificfaiones que se pueden hacer en la KB a partir de una sola cláusula
    def simplificacion_unica(kb, i, tipo, no_tipo_1, no_tipo_2):
        to_add = [] #Lista de cosas que hay que añadir a la base de conocimientos después de la resolución
        if tipo in kb[i]:
            #Si nos dice que hay algo en esa casilla intentamos hacer resolución e incluir información nueva
            if kb[i][tipo][1] == True:
                #Si hay un demogorgon en una casilla, no puede haber nada más
                if {no_tipo_1: [kb[i][tipo][0], False]} not in kb:
                    kb.append({no_tipo_1: [kb[i][tipo][0], False]})
                if {no_tipo_2: [kb[i][tipo][0], False]} not in kb:
                    kb.append({no_tipo_2: [kb[i][tipo][0], False]})
            #Hacemos resolución
            if kb[i][tipo][1] == True or kb[i][tipo][1] == False:
                for j in range(len(kb)):
                    #Buscamos otras afirmaciones que sean varias posibilidades, o OR
                    if tipo in kb[j] and j != i and kb[j][tipo][1] != True and kb[j][tipo][1] != False:
                        #Si hay información de esto en la misma casilla, podemos hacer resolución
                        for k in range(len(kb[j][tipo])):
                            try: #Al eliminar un elemento de la lista, se desplaza el índice y puede dar error de indice fuera de rango
                                if kb[j][tipo][k] == kb[i][tipo][0] and kb[i][tipo][1] == False:
                                    #Elimino la información de que hay un demogorgon en la casilla
                                    kb[j][tipo].pop(k)
                                    k-=1
                                    #Si queda una sola casilla, la simplifico
                                    if len(kb[j][tipo]) == 1:
                                        kb[j][tipo].append(True)
                                #Si se que en una de las casillas hay un demogorgon, se que el resto son falsas
                                elif kb[j][tipo][k] == kb[i][tipo][0] and kb[i][tipo][1] == True:
                                    for pos in kb[j][tipo]:
                                        if pos != kb[i][tipo][0]:
                                            to_add.append({tipo: [pos, False]})
                                    #Cambio esta afirmación por el último to add para eliminarla y no interferir en el otro bucle
                                    this_add = to_add.pop(-1)
                                    kb[j] = this_add
                            except:
                                pass
        #Añado la información que necesite
        for add in to_add:
            if add not in kb:
                kb.append(add)

    #Esta función pasa por la kb y simplifica las reglas
    for i in range(len(kb)):
        simplificacion_unica(kb, i, "D", "S", "A")
        simplificacion_unica(kb, i, "S", "A", "D")
        simplificacion_unica(kb, i, "A", "D", "S")
    #Eliminamos posibles duplicados
    for i in range(len(kb)):
        for j in range(len(kb)):
            try:
                if i != j and kb[i] == kb[j]:
                    kb.pop(j)
            except:
                pass
    return kb

def rellenar_base_conocimientos(kb, pos, sensaciones, estado):
    #Añade a la base de conocimientos las sensaciones que se han dado en esa casilla
    #Primero averiguo con cuantas casillas está pegada la casilla, puede ser de 2 a 4
    pos_posibles = []
    if pos[0] > 0:
        pos_posibles.append((pos[0]-1, pos[1]))
    if pos[0] < 4:
        pos_posibles.append((pos[0]+1, pos[1]))
    if pos[1] > 0:
        pos_posibles.append((pos[0], pos[1]-1))
    if pos[1] < 4:
        pos_posibles.append((pos[0], pos[1]+1))
    #Ahora añado las sensaciones a la base de conocimientos
    #No hay sensaciones, por lo que las casillas colindantes no tienen nada
    #Elimino "Hay una luz muy tenue" y "Hay algo de luz" porque no son relevantes
    sensaciones = [i for i in sensaciones if i != "Hay una luz muy tenue" and i != "Hay algo de luz"]
    n_Sensaciones = 0
    for i in sensaciones:
        if i!=None:
            n_Sensaciones+=1
    #En la casilla actual no hay nada, salvo que sea la salida si el estado es "Win"
    win = False if estado != "Win" else True
    kb.append({"D": [pos, False]})
    kb.append({"S": [pos, win]})
    kb.append({"A": [pos, False]})
    if n_Sensaciones == 0:
        for i in pos_posibles:
            kb.append({"D": [i, False]})
            kb.append({"S": [i, False]})
            kb.append({"A": [i, False]})
    #Añaado las sensaciones a la base de conocimientos
    for i in range(len(sensaciones)):
        if sensaciones[i] == "Hay mucha luz":
            informacion = {"S": pos_posibles}
            kb.append(informacion)
        elif sensaciones[i] == "Sientes una leve brisa":
            informacion = {"A": pos_posibles}
            kb.append(informacion)
        elif sensaciones[i] == "Sientes un cosquilleo en la nuca":
            informacion = {"D": pos_posibles}
            kb.append(informacion)
    #Hago la lógica de la base de conocimientos después de añadir la información
    kb = desarrollar_base_conocimientos(kb)
    return kb

#Función para recomendar el movimiento más óptimo que el jugador debe hacer en el próximo turno
def recomendacion_prox_movimiento(kb, mapa, demogorgon_killed):
    #Esta función devuelve la casilla a la que se debería mover el jugador
    #Primero obtengo el mapa lógico
    mapa_logico = obtener_mapa_logico(kb)
    pos_seguras = []
    pos_peligrosas = []
    pos_exploradas = []
    pos_demo = None
    pos_salida = None
    #D es 1, A es 2, S es 3, 4 es ! y 5 es ?
    #-3 es seguro
    for i in range(5):
        for j in range(5):
            #Si la posición es segura la añado a la lista de posiciones seguras
            if mapa_logico[i][j] == -3 or mapa_logico[i][j] == 5 or mapa_logico[i][j] == 3:
                pos_seguras.append((i,j))
            #Puede que haya que pasar por una posición peligrosa para llegar a una segura
            elif mapa_logico[i][j] == 4:
                pos_peligrosas.append((i,j))
            #Si la posición es explorada la añado a la lista de posiciones exploradas
            if mapa[i][j] >= 4:
                pos_exploradas.append((i,j))
            if mapa[i][j] == 4:
                pos_jugador = (i,j)
            if mapa_logico[i][j] == 1:
                pos_demo = (i,j)
            if mapa_logico[i][j] == 3:
                pos_salida = (i,j)
            if pos_salida == None and mapa[i][j] == 5:
                pos_salida = (i,j)
    #Compruebo si debo ir al demogorgon o a la salida
    if demogorgon_killed and pos_salida != None:
        pos_final = pos_salida
    elif pos_demo != None and not demogorgon_killed:
        pos_final = pos_demo
    #Si no debo ir al demogorgon o a la salida, debo ir a una posición segura para expandir el mapa
    else:
        pos_objetiivo = []
        #Las posiciones objetivo son las seguras que no estén exploradas
        for i in pos_seguras:
            if i not in pos_exploradas:
                pos_objetiivo.append(i)
        #Si no hay posiciones objetivo, las posiciones objetivo son las peligrosas
        if len(pos_objetiivo) == 0 or pos_objetiivo[0] == None:
            pos_objetiivo = pos_peligrosas
        #La posición objetoivo será la más cercana a la posición del jugador
        #Distancia manhattan
        def manhattan(pos1, pos2):
            return abs(pos1[0]-pos2[0]) + abs(pos1[1]-pos2[1])
        pos_final = pos_objetiivo[0]
        distancia = manhattan(pos_jugador, pos_objetiivo[0])
        for i in pos_objetiivo:
            if manhattan(pos_jugador, i) < distancia:
                distancia = manhattan(pos_jugador, i)
                pos_final = i
    #Queremos ir a la posición objetivo, pero hay que averiguar un camino seguro hasta allí
    #Función de búsqueda para encontrar la ruta más corta pasando sólo por posiciones seguras
    def buscar_ruta_optima(pos, destino, aux):
        pos_posibles = deepcopy(aux)
        pos_posibles.remove(pos)
        if pos == destino:
            return [pos]
        if len(pos_posibles) == 0:
            return None
        #Busqueda en anchura para encontrar la ruta más corta
        #Primero obtengo las posiciones posibles
        posibles = []
        der = (pos[0], pos[1]+1)
        izq = (pos[0], pos[1]-1)
        arriba = (pos[0]-1, pos[1])
        abajo = (pos[0]+1, pos[1])
        if der in pos_posibles:
            posibles.append(der)
        if izq in pos_posibles:
            posibles.append(izq)
        if arriba in pos_posibles:
            posibles.append(arriba)
        if abajo in pos_posibles:
            posibles.append(abajo)

        #Ahora busco la ruta más corta con recursión
        ruta = None
        for i in posibles:
            ruta_i = buscar_ruta_optima(i, destino, pos_posibles)
            if ruta_i != None and (ruta == None or len(ruta_i) < len(ruta)):
                ruta_i.append(pos)
                ruta = ruta_i
        return ruta
    #Obtengo el camino óptimo hasta el destino
    pos_seguras.append(pos_jugador)
    pos_seguras.append(pos_final)
    pos_seguras = list(set(pos_seguras))
    camino_optimo = buscar_ruta_optima(pos_jugador, pos_final, pos_seguras)
    
    #Si el camino óptimo es None, no hay camino seguro hasta el destino
    if camino_optimo == None:
        print("No hay camino seguro hasta el objetivo")
    else:
        dispara = ""
        camino_optimo.reverse()
        pos_siguiente = camino_optimo[1]
        #Averiguo si debo disparar
        if pos_demo == pos_siguiente:
            dispara = " y dispara"
        #Averiguo si es derecha, izquierda, arriba o abajo
        if pos_siguiente[0] == pos_jugador[0]:
            if pos_siguiente[1] > pos_jugador[1]:
                ir = "Derecha" + dispara
            else:
                ir = "Izquierda" + dispara
        else:
            if pos_siguiente[0] > pos_jugador[0]:
                ir = "Abajo" + dispara
            else:
                ir = "Arriba" + dispara
        print(" ->Recomendación: " + ir)
        print()