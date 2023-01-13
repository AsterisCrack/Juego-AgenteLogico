
import random
import numpy as np
import os
from copy import deepcopy

#DEFINO LAS PROBABILIDADES COMO VARIABLES GLOBALES
Pd = 0.6 #Probabilidad de verdadero positivo al sentir a un demogorgon
Qd = 0.2 #Probabilidad de falso positivo al sentir a un demogorgon
Pa = 0.8 #Probabilidad de verdadero positivo al sentir a un agujero
Qa = 0.1 #Probabilidad de falso positivo al sentir a un agujero
Ps = 0.9 #Probabilidad de verdadero positivo al sentir a una salida
Qs = 0.05 #Probabilidad de falso positivo al sentir a una salida
Pr = 0.85 #Probabilidad de acertar el disparo
GoForDemogorgon = 0.7 #Probabilidad mínima para ir a por el demogorgon
#Abro config.txt para establecer las variables de probabilidad
if os.path.exists("config.txt"):
    with open("config.txt", "r") as f:
        lineas = f.readlines()
        for linea in lineas:
            linea = linea.strip()
            if linea.startswith("Pd"):
                Pd = float(linea.split("=")[1])
            elif linea.startswith("Qd"):
                Qd = float(linea.split("=")[1])
            elif linea.startswith("Pa"):
                Pa = float(linea.split("=")[1])
            elif linea.startswith("Qa"):
                Qa = float(linea.split("=")[1])
            elif linea.startswith("Ps"):
                Ps = float(linea.split("=")[1])
            elif linea.startswith("Qs"):
                Qs = float(linea.split("=")[1])
            elif linea.startswith("Pr"):
                Pr = float(linea.split("=")[1])
            elif linea.startswith("GoForDemogorgon"):
                GoForDemogorgon = float(linea.split("=")[1])

def crear_mapa_Sensaciones(mapa):
    #Crea un mapa con las sensaciones del jugador teniendo en cuenta las probabilidades asociadas a cada sensación
    def casilla_colindante(pos):
        #Devuelve lo que haya en las casillas colindantes
        izq = (pos[0],pos[1]-1)
        der = (pos[0],pos[1]+1)
        arr = (pos[0]-1,pos[1])
        aba = (pos[0]+1,pos[1])
        colindantes = []
        if pos_valida(izq) and mapa[izq] != 0 and mapa[izq] != 4:
            colindantes.append(mapa[izq])
        if pos_valida(der) and mapa[der] != 0 and mapa[der] != 4:
            colindantes.append(mapa[der])
        if pos_valida(arr) and mapa[arr] != 0 and mapa[arr] != 4:
            colindantes.append(mapa[arr])
        if pos_valida(aba) and mapa[aba] != 0 and mapa[aba] != 4:
            colindantes.append(mapa[aba])
        return colindantes
    #Que sea un array con listas, no numeros
    mapa_sensaciones = np.zeros((5,5), dtype=object)
    for i in range(5):
        for j in range(5):
            mapa_sensaciones[i,j] = []
            #Relleno los verdaderos positivos:
            colindantes = casilla_colindante((i,j))
            #Hay un demogorgon en la casilla
            if 1 in colindantes:
                #Tiro probabilidad
                if random.random() < Pd:
                    mapa_sensaciones[i,j].append(1)
            #Hay una salida en la casilla
            if 3 in colindantes:
                #Tiro probabilidad
                if random.random() < Ps:
                    mapa_sensaciones[i,j].append(3)
            #Hay agujeros en la casilla
            n_agujeros = colindantes.count(2)
            for agujero in range(n_agujeros):
                #Tiro probabilidad
                if random.random() < Pa and 2 not in mapa_sensaciones[i,j]:
                    mapa_sensaciones[i,j].append(2)

            #Relleno los falsos positivos:
            if 1 not in colindantes:
                #Tiro probabilidad
                if random.random() < Qd:
                    mapa_sensaciones[i,j].append(1)
            if 3 not in colindantes:
                #Tiro probabilidad
                if random.random() < Qs:
                    mapa_sensaciones[i,j].append(3)
            if n_agujeros == 0:
                #Tiro probabilidad
                if random.random() < Qa:
                    mapa_sensaciones[i,j].append(2)
    return mapa_sensaciones

#Clase para manejar la base de conocimientos
class KB_probabilistica:
    def __init__(self):
        #Mapa de probabilidades que almacena la probabilidad de que haya algo en cada casilla
        self.mapa_probabilidades = np.zeros((5,5), dtype=object)
        for i in range(5):
            for j in range(5):
                self.mapa_probabilidades[i,j] = {"D": 1/25, "S": 1/25, "A": 3/25}
        #Mapa de casillas por las que he pasado, 0 false 1 true
        self.mapa_explorado = np.zeros((5,5), dtype=int)

    def inferencia_demo(self, casilla, sentido):
        #Hace inferencia para un demogorgon en una casilla
        #Esta función se llama cuando sentimos, o no un demogorgon en una casilla
        #Actualiza el mapa de probabilidades teniendo en cuenta Pd, Qd 
        #Caso 1: Hemos sentido al demogorgon
        p_demogo = self.mapa_probabilidades[casilla]["D"] #Prior de que haya un demogorgon en esta casilla
        #Calculo el posterior
        if sentido:
            posterior = (p_demogo * Pd) / (p_demogo * Pd + (1-p_demogo) * Qd)
        else:
            posterior = (p_demogo * (1-Pd)) / (p_demogo * (1-Pd) + (1-p_demogo) * (1-Qd))
        #Actualizo la probabilidad de que haya un demogorgon en esta casilla
        self.mapa_probabilidades[casilla]["D"] = posterior
        #Reajusto la probabilidad
        self.ajuste_probabilidad(casilla, "D", p_demogo-posterior)
    
    def inferencia_salida(self, casilla, sentido):
        #La misma idea que el demogorgon
        p_salida = self.mapa_probabilidades[casilla]["S"]
        if sentido:
            posterior = (p_salida * Ps) / (p_salida * Ps + (1-p_salida) * Qs)
        else:
            posterior = (p_salida * (1-Ps)) / (p_salida * (1-Ps) + (1-p_salida) * (1-Qs))
        self.mapa_probabilidades[casilla]["S"] = posterior
        #Reajusto la probabilidad
        self.ajuste_probabilidad(casilla, "S", p_salida-posterior)

    def inferencia_brisa(self, casilla, sentido):
        #La misma idea que el demogorgon
        p_agujero = self.mapa_probabilidades[casilla]["A"]
        if sentido:
            posterior = (p_agujero * Pa) / (p_agujero * Pa + (1-p_agujero) * Qa)
        else:
            posterior = (p_agujero * (1-Pa)) / (p_agujero * (1-Pa) + (1-p_agujero) * (1-Qa))
        self.mapa_probabilidades[casilla]["A"] = posterior
        #Reajusto la probabilidad
        self.ajuste_probabilidad(casilla, "A", p_agujero-posterior)

    def ajuste_probabilidad(self, repartido_desde, tipo, p_a_repartir):
        #Esta función reajusta las probabilidades
        #Se llama al cambiar la probabilidad de algo para reajustar todo el tablero y que la probabilidad siempre sume 1
        #Reparte la diferencia entre el valor previo y el nuevo de la casilla proporcionalmente
        for i in range(5):
            for j in range(5):
                if (i,j) != repartido_desde:
                    P = p_a_repartir/3 if tipo == "A" else p_a_repartir
                    if p_a_repartir > 0:
                        self.mapa_probabilidades[i,j][tipo] = self.mapa_probabilidades[i,j][tipo]/(1-P)
                    else:
                        self.mapa_probabilidades[i,j][tipo] = self.mapa_probabilidades[i,j][tipo]*(1+P)

    def certeza(self, casilla, tipo, hay):
        #Esta función se llama cuando hay certeza de que hay algo en una casilla, ya sea un demogorgon o una salida
        #Actualiza el mapa de probabilidades
        otros_tipos = ["D", "S", "A"]
        otros_tipos.remove(tipo)
        for i in range(5):
            for j in range(5):
                if (i,j) == casilla:
                    if hay:
                        self.mapa_probabilidades[i,j][tipo] = 1
                        self.ajuste_probabilidad(casilla, otros_tipos[0], self.mapa_probabilidades[i,j][otros_tipos[0]])
                        self.ajuste_probabilidad(casilla, otros_tipos[1], self.mapa_probabilidades[i,j][otros_tipos[1]])
                        self.mapa_probabilidades[i,j][otros_tipos[0]] = 0
                        self.mapa_probabilidades[i,j][otros_tipos[1]] = 0
                    else:
                        self.ajuste_probabilidad(casilla, tipo, self.mapa_probabilidades[i,j][tipo])
                        self.mapa_probabilidades[i,j][tipo] = 0
                elif hay:
                    self.mapa_probabilidades[i,j][tipo] = 0

    def pasar_por(self, casilla):
        #Función que establece que se ha pasado por esa casilla
        self.mapa_explorado[casilla] = 1

#Funcion que devuelve si una posición existe dentro del tablero de juego
def pos_valida(pos):
            return pos[0] >= 0 and pos[0] < 5 and pos[1] >= 0 and pos[1] < 5

#Función para imprimir el mapa de probabilidades
def imprimir_mapa_logico(kb):
    mapa = kb.mapa_probabilidades
    mapa_imprimir = []
    #Es más grande que el mapa de juego para que se vea todo bien, es algo engorroso
    mapa_imprimir.append("┏━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┓\n")
    for i in range(5):
        for tipo in mapa[i,0].keys():
            for j in range(5):
                #Imprimo las probabilidades de cada cosa, con dos decimales
                mapa_imprimir.append("┃ {} {:.2f} ".format(tipo, mapa[i,j][tipo]))
            mapa_imprimir.append("┃\n")
        if i < 4:
            mapa_imprimir.append("┣━━━━━━━━╋━━━━━━━━╋━━━━━━━━╋━━━━━━━━╋━━━━━━━━┫\n")
    mapa_imprimir.append("┗━━━━━━━━┻━━━━━━━━┻━━━━━━━━┻━━━━━━━━┻━━━━━━━━┛\n")
    return mapa_imprimir

#Imprime la tabla con el histórico de sensaciones
#Funciona de forma similar a la función de mismo nombre en la Versión 1
def imprimir_tabla_Sensaciones(mapa, sensaciones):
    mapa_imprimir = []
    max_casilla = 4
    casillas_numeradas = []
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
    
    for i in pos_visitadas:
        casilla = int(mapa[i]) if int(mapa[i]) != 4 else int(casilla_jugador)
        s = " " + str(int(casilla-4)) + " "
        counter += 1
        if len(s) == 4:
            s = " " + str(casilla-4)
        mapa_imprimir.append(f"┃{s}┃")
        #La diferencia con la versión 1 es que las sensaciones se almacenan de forma ligeramente distinta
        if 2 in sensaciones[i]:
            mapa_imprimir.append("  X  ")
        else:
            mapa_imprimir.append("     ")
        mapa_imprimir.append("┃")
        if 1 in sensaciones[i]:
            mapa_imprimir.append("    X     ")
        else:
            mapa_imprimir.append("          ")
        mapa_imprimir.append("┃")
        if 3 in sensaciones[i]:
            mapa_imprimir.append(" X ")
        else:
            mapa_imprimir.append("   ")
        mapa_imprimir.append("┃\n")
        if counter < len(pos_visitadas):
            mapa_imprimir.append("┣━━━╋━━━━━╋━━━━━━━━━━╋━━━┫\n")
    mapa_imprimir.append("┗━━━┻━━━━━┻━━━━━━━━━━┻━━━┛\n")
    return mapa_imprimir

def sentir(mapa, mapa_sensaciones):
    #Devuelve un alista con las sensaciones que da esa casilla
    pos_jugador = (0,0)
    for i in range(5):
        for j in range(5):
            if mapa[i,j] == 4:
                pos_jugador = (i,j)
    sensaciones = mapa_sensaciones[pos_jugador]
    sensaciones = list(set(sensaciones))
    for i in range(len(sensaciones)):
        if sensaciones[i] == 1:
            sensaciones[i] = "Sientes un cosquilleo en la nuca"
        elif sensaciones[i] == 2:
            sensaciones[i] = "Sientes una leve brisa"
        #En la versión probabilística sñolo hay un nivel de luz
        elif sensaciones[i] == 3:
            sensaciones[i] = "Hay algo de luz"
    return sensaciones

#Imprime todos los mapas uno al lado del otro
def imprimir_estado_juego(sensaciones, mapa, mapa_logico):
    sensaciones = "".join(sensaciones)
    sensaciones = sensaciones.split("\n")[:-1]
    mapa = "".join(mapa)
    mapa = mapa.split("\n")[:-1]
    mapa_logico = "".join(mapa_logico)
    mapa_logico = mapa_logico.split("\n")
    if len(sensaciones) < len(mapa_logico):
        for i in range(len(sensaciones)-1, len(mapa_logico)):
            sensaciones.append("                          ")
    if len(mapa) < len(mapa_logico):
        for i in range(len(mapa)-1, len(mapa_logico)):
            mapa.append("                     ")
    for i in range(len(sensaciones)):
        s = sensaciones[i].replace("\n", "")
        s += " "*(5)
        try:
            s += mapa[i]
        except:
            s += "                          "
        s += " "*(5)
        try:
            s += mapa_logico[i]
        except:
            pass
        print(s)
    print("")

def rellenar_base_conocimientos(kb, pos_jugador, mapa_sensaciones, mapa, estado):
    #Añade a la base de conocimientos las sensaciones que se han dado en esa casilla
    #Luego hace las inferencias correspondientes
    #Primero averiguo si esta casilla ya ha sido explorada:
    pasado = True if kb.mapa_explorado[pos_jugador] == 1 else False
    kb.pasar_por(pos_jugador)
    #Si no ha sido explorada, hago las inferencias necesarias a la base de conociminetos
    if not pasado:
        #Averiguo que sensaciones he tenido y cuales no
        sensaciones = mapa_sensaciones[pos_jugador]
        sensaciones = list(set(sensaciones))
        #Hago las inferencias
        sentido_demo = True if 1 in sensaciones else False
        sentido_brisa = True if 2 in sensaciones else False
        sentido_salida = True if 3 in sensaciones else False
        casillas_a_inferenciar = []
        #Derecha 
        if pos_valida((pos_jugador[0], pos_jugador[1]+1)):
            casillas_a_inferenciar.append((pos_jugador[0], pos_jugador[1]+1))
        #Izquierda
        if pos_valida((pos_jugador[0], pos_jugador[1]-1)):
            casillas_a_inferenciar.append((pos_jugador[0], pos_jugador[1]-1))
        #Arriba
        if pos_valida((pos_jugador[0]-1, pos_jugador[1])):
            casillas_a_inferenciar.append((pos_jugador[0]-1, pos_jugador[1]))
        #Abajo
        if pos_valida((pos_jugador[0]+1, pos_jugador[1])):
            casillas_a_inferenciar.append((pos_jugador[0]+1, pos_jugador[1]))
        for casilla in casillas_a_inferenciar:
            kb.inferencia_salida(casilla, sentido_salida)
            kb.inferencia_demo(casilla, sentido_demo)
            kb.inferencia_brisa(casilla, sentido_brisa)

        #Si hay certeza de algo lo añado también
        if estado == "Win":
            kb.certeza(pos_jugador, "S", True)
        elif estado == "Demogorgon":
            kb.certeza(pos_jugador, "D", True)
        #Si no, se que aquí no hay nada
        else:
            kb.certeza(pos_jugador, "D", False)
            kb.certeza(pos_jugador, "S", False)
            kb.certeza(pos_jugador, "A", False)

def recomendacion_prox_movimiento(kb, demogorgon_killed, mapa):
    #Esta función devuelve la casilla a la que se debería mover el jugador
    #Primero obtengo el mapa lógico
    pos_seguras = []
    pos_peligrosas = []
    pos_exploradas = []
    pos_demo = None
    pos_salida = None
    mapa_logico = kb.mapa_probabilidades
    #Relleno posiciones exploradas
    for i in range(5):
        for j in range(5):
            if kb.mapa_explorado[i,j] == 1:
                pos_exploradas.append((i,j))
            #Establezco cuándo intentar matar al demogorgon:
            #Es un valor totalmente aleatorio establecido por el usuario en la configuración
            if mapa_logico[i,j]["D"] >= GoForDemogorgon:
                pos_demo = (i,j)
            if mapa_logico[i,j]["S"] == 1:
                pos_salida = (i,j)
            if mapa[i,j] == 4:
                pos_jugador = (i,j)
    #Las posiciones peligrosas serán las posiciones a las que puedo llegar directamente desde las exploradas, pero no han sido exploradas
    for i in pos_exploradas:
        #Izquierda
        if (i[0]-1, i[1]) not in pos_exploradas and pos_valida((i[0]-1, i[1])):
            pos_peligrosas.append((i[0]-1, i[1]))
        #Derecha
        if (i[0]+1, i[1]) not in pos_exploradas and pos_valida((i[0]+1, i[1])):
            pos_peligrosas.append((i[0]+1, i[1]))
        #Arriba
        if (i[0], i[1]-1) not in pos_exploradas and pos_valida((i[0], i[1]-1)):
            pos_peligrosas.append((i[0], i[1]-1))
        #Abajo
        if (i[0], i[1]+1) not in pos_exploradas and pos_valida((i[0], i[1]+1)):
            pos_peligrosas.append((i[0], i[1]+1))

    #D es 1, A es 2, S es 3, 4 es ! y 5 es ?
    #-3 es seguro
    if (demogorgon_killed or demogorgon_killed == "Impossible") and pos_salida != None:
        pos_final = pos_salida
    elif pos_demo != None and not demogorgon_killed:
        pos_final = pos_demo
    else:
        #Mi posición objetivo será la más segura posible
        posibilidades_max_morir = []
        for i in range(len(pos_peligrosas)):
            pos_i = pos_peligrosas[i]
            posibilidades_max_morir.append(kb.mapa_probabilidades[pos_i[0],pos_i[1]]["D"])
            if posibilidades_max_morir[i] < kb.mapa_probabilidades[pos_i[0],pos_i[1]]["A"]:
                posibilidades_max_morir[i] = kb.mapa_probabilidades[pos_i[0],pos_i[1]]["A"]
        probabilidades_asociadas_a_casillas = []
        for i in range(len(pos_peligrosas)):
            probabilidades_asociadas_a_casillas.append((pos_peligrosas[i], posibilidades_max_morir[i]))
        probabilidades_asociadas_a_casillas.sort(key=lambda x: x[1])

        #La posición objetivo será la primera ya que es la más segura
        pos_final = probabilidades_asociadas_a_casillas[0][0]

    #Queremos ir a la posición objetivo, pero hay que averiguar un camino seguro hasta allí
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
    pos_exploradas.append(pos_jugador)
    pos_exploradas.append(pos_final)
    pos_seguras = list(set(pos_exploradas))
    camino_optimo = buscar_ruta_optima(pos_jugador, pos_final, pos_seguras)
    #Si el camino óptimo es None, no hay camino seguro hasta el destino
    if camino_optimo == None:
        print("No hay camino seguro hasta el objetivo")
    else:
        dispara = ""
        camino_optimo.reverse()
        pos_siguiente = camino_optimo[1]
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
        p_morir = 0
        probabilidades_asociadas_pos_siguiente = mapa_logico[pos_siguiente]
        if not demogorgon_killed:
            p_morir = probabilidades_asociadas_pos_siguiente["D"] + probabilidades_asociadas_pos_siguiente["A"]
        else:
            p_morir = probabilidades_asociadas_pos_siguiente["A"]

        print(" ->Recomendación: {} con una probabilidad de {:.2f} de perder.".format(ir, p_morir))
        print()  

#Funciones usadas por el main para obtener las probabilidades
def obtener_Pr():
    return random.random() <= Pr

def obtener_probabilidades():
    return [Pd, Qd, Pa, Qa, Ps, Qs, Pr]