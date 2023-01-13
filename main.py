
import os, sys, signal
from typing import List, Dict, Tuple, Callable, Any
import numpy as np
import random
from copy import deepcopy
import V1
import V2

#MAnejo el ctrl+c
def signal_hanler(signal, frame):
    print("\nSaliste del videojuego...\n")
    sys.exit(0)
signal.signal(signal.SIGINT, signal_hanler)

clear_console = lambda: os.system('cls')

def imprimir_menu_principal():   
    print("                                                                                                                                               ")  
    print("▓█████▄ ▓█████  ███▄ ▄███▓ ▒█████    ▄████  ▒█████   ██▀███    ▄████  ▒█████   ███▄    █    ▓█████   ██████  ▄████▄   ▄▄▄       ██▓███  ▓█████ ") 
    print("▒██▀ ██▌▓█   ▀ ▓██▒▀█▀ ██▒▒██▒  ██▒ ██▒ ▀█▒▒██▒  ██▒▓██ ▒ ██▒ ██▒ ▀█▒▒██▒  ██▒ ██ ▀█   █    ▓█   ▀ ▒██    ▒ ▒██▀ ▀█  ▒████▄    ▓██░  ██▒▓█   ▀ ")
    print("░██   █▌▒███   ▓██    ▓██░▒██░  ██▒▒██░▄▄▄░▒██░  ██▒▓██ ░▄█ ▒▒██░▄▄▄░▒██░  ██▒▓██  ▀█ ██▒   ▒███   ░ ▓██▄   ▒▓█    ▄ ▒██  ▀█▄  ▓██░ ██▓▒▒███   ")
    print("░▓█▄   ▌▒▓█  ▄ ▒██    ▒██ ▒██   ██░░▓█  ██▓▒██   ██░▒██▀▀█▄  ░▓█  ██▓▒██   ██░▓██▒  ▐▌██▒   ▒▓█  ▄   ▒   ██▒▒▓▓▄ ▄██▒░██▄▄▄▄██ ▒██▄█▓▒ ▒▒▓█  ▄ ")
    print("░▒████▓ ░▒████▒▒██▒   ░██▒░ ████▓▒░░▒▓███▀▒░ ████▓▒░░██▓ ▒██▒░▒▓███▀▒░ ████▓▒░▒██░   ▓██░   ░▒████▒▒██████▒▒▒ ▓███▀ ░ ▓█   ▓██▒▒██▒ ░  ░░▒████▒")
    print("▒▒▓  ▒ ░░ ▒░ ░░ ▒░   ░  ░░ ▒░▒░▒░  ░▒   ▒ ░ ▒░▒░▒░ ░ ▒▓ ░▒▓░ ░▒   ▒ ░ ▒░▒░▒░ ░ ▒░   ▒ ▒    ░░ ▒░ ░▒ ▒▓▒ ▒ ░░ ░▒ ▒  ░ ▒▒   ▓▒█░▒▓▒░ ░  ░░░ ▒░ ░ ")
    print("░ ▒  ▒  ░ ░  ░░  ░      ░  ░ ▒ ▒░   ░   ░   ░ ▒ ▒░   ░▒ ░ ▒░  ░   ░   ░ ▒ ▒░ ░ ░░   ░ ▒░    ░ ░  ░░ ░▒  ░ ░  ░  ▒     ▒   ▒▒ ░░▒ ░      ░ ░  ░ ")
    print("░ ░  ░    ░   ░      ░   ░ ░ ░ ▒  ░ ░   ░ ░ ░ ░ ▒    ░░   ░ ░ ░   ░ ░ ░ ░ ▒     ░   ░ ░       ░   ░  ░  ░  ░          ░   ▒   ░░          ░    ")
    print(" ░       ░  ░       ░       ░ ░        ░     ░ ░     ░           ░     ░ ░           ░       ░  ░      ░  ░ ░            ░  ░            ░  ░  ")
    print("                                                                                                                                               ")  
    print("                                                                                          ╓▓█╗                                                 ")       
    print("                                                                                        φ█████▓          ▐L                                    ")     
    print("                                                                                       ▐▓██████▌   g▄▓████▌                                    ")   
    print("                                                                                        ▓██████▌ ▓████████▌                                    ") 
    print("                      ┏━━┳━━━━━━━━━━━━━━━━━━━━━━━┓                            ,╓φ▄▄╖    ▓▓██▓▓█▓ ▓█████▓█▓                                     ")
    print("                      ┃1.┃ Fácil                 ┃                        ╗▄▄▓███████▄▄╓▓▓██████▓███████▓                                      ") 
    print("                      ┣━━╋━━━━━━━━━━━━━━━━━━━━━━━┫      @╖                  ▓▓███████████▓████████████▓▀                                       ")
    print("                      ┃2.┃ Normal                ┃       ▓▓                   ▀▓▓▓▓██▓████████████▓█▓                                          ")
    print("                      ┣━━╋━━━━━━━━━━━━━━━━━━━━━━━┫      ╓ ▀▓╖                    ``   ▓██████████▓███▄                                         ")
    print("                      ┃3.┃ Difícil               ┃      ╙▒▓▓▓▓, ,,╓╖                ,▓██▓███▓▓▓▓██████▓▓▄                                      ")
    print("                      ┣━━╋━━━━━━━━━━━━━━━━━━━━━━━┫     ╓╖▓▓▓▓▓▓█▓█╝              ╔▓▓█████▓▓▓██▓██▓█▓███▓█▓                                     ")
    print("                      ┃4.┃ Dificultad ĐɆ₥Ø₲ØⱤ₲Ø₦ ┃     `╨╣▓▓▓▓▓▓▓                ▓▓▓██████▓██████▓▓▓████▓█L                                    ")
    print("                      ┣━━╋━━━━━━━━━━━━━━━━━━━━━━━┫       ▐▓▓▓▓▓▓▓L              ,▓▓▓██▓██▓████▓████▓▓▓▓▓█▓▓m                                   ")
    print("                      ┃5.┃ SALIR                 ┃         ""╙▓▓▓▌            ╓▓╬▓▓▓█▓▓███▓╢▓▓▓╫▓▓▓▓▓▓█▓▓▓▓                                    ")
    print("                      ┗━━┻━━━━━━━━━━━━━━━━━━━━━━━┛            ▓▓▓▓,         ╓▓▓▓▓▓▓▓▓▓█▓▓╢╢╣▓▓╫╣╢╣▓▓▓▓▓▓▓▓▓▓                                   ")
    print("                                                               ▓▓▓╣╕   ,╓╗@╢╢▓▓▓▓▓▓█▓▓▓▓▓▓▓▓▓▓▓▓╣╢╢▓▓▓▓▓▓▓▓▓▓                                  ")
    print("                                                               ▓▓▓▓▓╥▓▓▓▓▓▓▓▓▓▓█▀▀▀██▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓█▓▓█▓▓▓                                 ")
    print("                                                                ▓▓▓▓▓▓▓▓▓▓▓▀▀'`     ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓╫▓▓  ▀▓▓▓▓▓                                ")
    print("                                                                ╚▓▓▓▀               ▓▓╣▓▓▓▓▓╣▓▓╢▓▓▒╢▓▓▓   ╙▓▓▓▓▓                               ")
    print("                                                                                    ▓▓▓▓╣╣▓▓▒╫╣╫▓▓▓▓▓▓╣     ▓▓╣▓▓╖                             ")
    print("                                                                                     ╚▀▀╩╩╩╩╝╝╩╩▀▀╩╩╩╜       ╙╩╩╩╩*                            ")

def instrucciones():
    print("┏━━━━━━━━━━━━━━━━━━━━━━━━━┓")
    print("┃ INSTRUCCIONES DEL JUEGO ┃")
    print("┗━━━━━━━━━━━━━━━━━━━━━━━━━┛")
    print()
    print("Escribe la dirección a la cual deseas moverte")
    print(" -> ARRIBA: U")
    print(" -> ABAJO: D")
    print(" -> IZQUIERDA: L")
    print(" -> DERECHA: R")
    print()
    print("Si, además de moverte, deseas disparar:")
    print(" -> Escribe la dirección seguida de un ESPACIO y una S")
    print()
    input("Pulsa ENTER para continuar\n")

def historia_modo1():
    print("Eres Spiderman.")
    print("Un enemigo poderoso, el DEMOGORGON, amenaza a la Tierra.")
    print("El Demogorgon se ha escondido en una cueva con muchos peligros, ten cuidado Spiderman.")
    print("Tu misión es encontrarlo y acabar con él para poder salir de la cueva victorioso.")
    print("En esta misión, ¡ayúdate de tu sentido arácnido para no caer en ningún agujero y encontrar al Demogorgon!")
    print("Por desgracia, sólo te queda un disparo del lanzatelarañas, ¡así que procura acertar!")
    print("Si fallas el disparo, huye a la salida y al menos sálvate tú.")                                                                        
    print("¡Buena suerte Spiderman!                #                                       ")
    print("                          &#             @          @                           ")
    print("                           %#            %         (.                           ")
    print("                             @.        @          .@                            ")
    print("                  @,          @@       @@        @&              @              ")
    print("                     @        @@@      /@@      @@@           @                 ")
    print("        ,@@%          ,@@&     *@@     @@,     #@@       .@@@.                  ")
    print("           &@@           @@@     *             %@.     @@@                      ")
    print("             %@@@@&              .#@@@@@@@@/        ,@@(              (@&%,     ")
    print("       @&        @@@@      (@@(((((&@(((((((@((@@            &@@@@@@%           ")
    print("         /@@@@          @#((((@(&&(((((((((((#@(((%@     @@@(                   ")
    print("              @.     @#((((((%((((((&%(%((((&%(#%((((@          %%%@@@@@#@#     ")
    print("                   @%((((((#((((((((((@@@@(((((((((&&(@%   @@@@@@@(             ")
    print("                 %@#((((((@(((((((((@@@@@@@@(((((&((((@%@                       ")
    print("                #@((((((@((((((((#%(@@@@@@@@@@((((#(((@(#,  .(                  ")
    print("               ,@(((((@(((%%&@@@@@##@@@@  %@@@@@&(@#((%(&@    ,.  .#@*   .@(    ")
    print("               @&(((@(((((((((#((((&@@@&     @@@@(@((@#((@                      ")
    print("               @((%(&((((((((#(((((@@@@%      &@@%&@@((@%@                      ")
    print("              /@#%(%&((((((((&(((((#@@@@@.    @@@@(@(@#%@   ,@@@@@@@,*,,        ")
    print("           @@(@(((@&%(((((((@((((#&@@@@@@@@@@@@%@&@@@@@@                  &@*   ")
    print("      %@@@(@%(((((@&#(((((%@%((((((((((##%#((@(((#@@  &     @@@@(               ")
    print("@@@@@@%(@((((#((((@@%%(((((((#(((((((((%((@((((((%@@ (           ** @/          ")
    print("((((&&((((((((%((%@@#((((((((#(((((((((@@&((((((%#@@                            ")
    print("((((((@((((((((@((@@@%((((((((%(((((@(((((((@((%&%@      @@@@*                  ")
    print("(((((((@(((((&(((@@@@@@#(((((((%#&((((((((((((%(@               @               ")
    print("((((((((&(@(((((((@@@@@@(((((@#((#@((((((((((%@     @@@           &@&           ")
    print("(((((((@@%((((((((&@@@@@@@@((((((((((#@((((%&         @@@@                      ")
    print("((((@((((((&#((((((@@@@@@@@@(((((((((((((@%               @.                    ")
    print("@&(((((((((((&(&%((((%@%@@   /@((((((((@                    *@                  ")
    print("&#@((((((((#@((((((@@@@@@@@       /@(                                           ")
    print("((((%&((@#(((((%@@#((@@@@@@@/                                                   ")
    print()
    input("Pulsa ENTER para continuar\n")

def historia_modo2():
    print("Antes de esconderse en la cueva, el Demogorgon y tú habéis tenido una dura pelea.")
    print("El Demogorgon ha conseguido herirte de gravedad, tu sentido arácnido no funciona correctamente.")
    print("Tu precisión tampoco es ideal.")
    probabilidades = V2.obtener_probabilidades()
    print()
    print(f"Si detectas a un DEMOGORGON hay un {probabilidades[0]:.2f} de que esté a tu lado, y un {probabilidades[1]:.2f} de que sólo sea tu imaginación.")
    print(f"Si detectas un AGUJERO hay un {probabilidades[2]:.2f} de que esté a tu lado, y un {probabilidades[3]:.2f} de que sólo sea tu imaginación.")
    print(f"Si detectas la SALIDA hay un {probabilidades[4]:.2f} de que esté a tu lado, y un {probabilidades[5]:.2f} de que sólo sea tu imaginación.")
    print(f"Tienes un {1-probabilidades[6]:.2f} de fallar tu único disparo.")
    print()
    input("Pulsa ENTER para continuar\n")

def historia_agente():
    print("Por suerte, te has traído a la misión las gafas del SEÑOR STARK.")
    print("E.D.I.T.H. te ayudará a detectar a los enemigos y a la salida.")
    print("¡Apóyate en su gran capacidad lógica para acabar con ese monstruo!")
    print()
    input("Pulsa ENTER para continuar\n")

def win_screen():
    clear_console()
    
    print("  ██╗   ██╗██╗ ██████╗████████╗ ██████╗ ██████╗ ██╗ █████╗ ██╗")
    print("  ██║   ██║██║██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗██║██╔══██╗██║")
    print("  ██║   ██║██║██║        ██║   ██║   ██║██████╔╝██║███████║██║")
    print("  ╚██╗ ██╔╝██║██║        ██║   ██║   ██║██╔══██╗██║██╔══██║╚═╝")
    print("   ╚████╔╝ ██║╚██████╗   ██║   ╚██████╔╝██║  ██║██║██║  ██║██╗")
    print("    ╚═══╝  ╚═╝ ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚═╝")   
    print()                                                      
    print("                        ¡Has ganado!")
    print("¡Has conseguido acabar con el demogorgon y escapar de la cueva!")
    print()
    input("Pulsa ENTER para continuar\n")

def lose_screen():
    clear_console()
    
    print("   ██░ ██  ▄▄▄        ██████     ███▄ ▄███▓ █    ██ ▓█████  ██▀███  ▄▄▄█████▓ ▒█████  ")
    print("  ▓██░ ██▒▒████▄    ▒██    ▒    ▓██▒▀█▀ ██▒ ██  ▓██▒▓█   ▀ ▓██ ▒ ██▒▓  ██▒ ▓▒▒██▒  ██▒")
    print("  ▒██▀▀██░▒██  ▀█▄  ░ ▓██▄      ▓██    ▓██░▓██  ▒██░▒███   ▓██ ░▄█ ▒▒ ▓██░ ▒░▒██░  ██▒")
    print("  ░▓█ ░██ ░██▄▄▄▄██   ▒   ██▒   ▒██    ▒██ ▓▓█  ░██░▒▓█  ▄ ▒██▀▀█▄  ░ ▓██▓ ░ ▒██   ██░")
    print("  ░▓█▒░██▓ ▓█   ▓██▒▒██████▒▒   ▒██▒   ░██▒▒▒█████▓ ░▒████▒░██▓ ▒██▒  ▒██▒ ░ ░ ████▓▒░")
    print("   ▒ ░░▒░▒ ▒▒   ▓▒█░▒ ▒▓▒ ▒ ░   ░ ▒░   ░  ░░▒▓▒ ▒ ▒ ░░ ▒░ ░░ ▒▓ ░▒▓░  ▒ ░░   ░ ▒░▒░▒░ ")
    print("   ▒ ░▒░ ░  ▒   ▒▒ ░░ ░▒  ░ ░   ░  ░      ░░░▒░ ░ ░  ░ ░  ░  ░▒ ░ ▒░    ░      ░ ▒ ▒░ ")
    print("   ░  ░░ ░  ░   ▒   ░  ░  ░     ░      ░    ░░░ ░ ░    ░     ░░   ░   ░      ░ ░ ░ ▒  ")
    print("   ░  ░  ░      ░  ░      ░            ░      ░        ░  ░   ░                  ░ ░  ")
    print()
    print("                                   ¡Has perdido!")
    print("                      ¡El Demogorgon ha conseguido atraparte!")
    print()
    input("Pulsa ENTER para continuar\n")

def neutral_screen():
    clear_console()
    
    print("███    ██ ███████ ██    ██ ████████ ██████   █████  ██          ███████ ███    ██ ██████  ██ ███    ██  ██████  ")
    print("████   ██ ██      ██    ██    ██    ██   ██ ██   ██ ██          ██      ████   ██ ██   ██ ██ ████   ██ ██       ")
    print("██ ██  ██ █████   ██    ██    ██    ██████  ███████ ██          █████   ██ ██  ██ ██   ██ ██ ██ ██  ██ ██   ███ ")
    print("██  ██ ██ ██      ██    ██    ██    ██   ██ ██   ██ ██          ██      ██  ██ ██ ██   ██ ██ ██  ██ ██ ██    ██ ")
    print("██   ████ ███████  ██████     ██    ██   ██ ██   ██ ███████     ███████ ██   ████ ██████  ██ ██   ████  ██████  ")
    print()                                                                                                                                                                      
    print("                              ¡Has conseguido escapar de la cueva!")
    print("                ¡Pero el Demogorgon sigue vivo y ten por seguro que volverá a por tí!")
    print()
    input("Pulsa ENTER para continuar\n")

def imprimir_historia(modo):
    clear_console()
    historia_modo1()
    clear_console()
    if modo == 3 or modo == 4:
        historia_modo2()
        clear_console()
    if modo == 1 or modo == 3:
        historia_agente()
        clear_console()
    instrucciones()
    clear_console()

#Función para pedir entrada del usuario en el menú principal
def pedir_entrada(texto: str, valores_validos: List)->str:
    s1 = "┏" + "━"*len(texto) + "┓"
    s2 = "┃" + texto + "┃"
    s3 = "┗" + "━"*len(texto) + "┛"
    print(s1)
    print(s2)
    print(s3)
    ok = False
    while not ok:
        inp = input(" -> ").strip().upper()
        if inp in valores_validos:
            ok = True
            return inp
        else:
            print("Valor no válido")

def crear_mapa():
    #Un array 5x5
    mapa = np.zeros((5,5))
    #El demogorgon se indica con un 1, hay 1 demogorgon
    #Los agujeros con un 2, hay 3 agujeros
    #La salida con un 3, hay 1 salida
    #El jugador con un 4, hay 1 jugador
    #El resto de casillas son 0
    mapa[4,0] = 1
    pos_demogorgon = (4,0)
    while pos_demogorgon == (4,0):
        pos_demogorgon = (random.randint(0,4),random.randint(0,4))
    mapa[pos_demogorgon] = 1
    for i in range(3):
        pos_agujero = (4,0)
        while pos_agujero == (4,0) or pos_agujero == pos_demogorgon or mapa[pos_agujero] == 2:
            pos_agujero = (random.randint(0,4),random.randint(0,4))
        mapa[pos_agujero] = 2
    pos_salida = (4,0)
    while pos_salida == (4,0) or mapa[pos_salida] != 0:
        pos_salida = (random.randint(0,4),random.randint(0,4))
    mapa[pos_salida] = 3
    pos_jugador = (4,0)
    mapa[pos_jugador] = 4
    mapa_copy = deepcopy(mapa)
    if not existe_solucion(mapa_copy, 3, 1):
        mapa = crear_mapa()
    return mapa

def existe_solucion(mapa, buscar, evitar):
    #Comprueba que exista un camino desde la salida hasta el jugador sin pasar por agujeros o el demogorgon
    #Devuelve True si existe solución y False si no existe solución
    #Busco la posicion del jugador en el mapa:
    pos_jugador = (0,0)
    for i in range(5):
        for j in range(5):
            if mapa[i,j] == 4:
                pos_jugador = (i,j)
    found = False
    #Movemos al jugador hacia todos los lados
    derecha = (pos_jugador[0],pos_jugador[1]+1)
    izquierda = (pos_jugador[0],pos_jugador[1]-1)
    arriba = (pos_jugador[0]-1,pos_jugador[1])
    abajo = (pos_jugador[0]+1,pos_jugador[1])
    #Compruebo si el jugador está en la salida al moverlo
    #Hay que tener en cuenta que se puede salir de los límites del mapa 
    if V1.pos_valida(derecha) and mapa[derecha] == buscar:
        found = True
    elif V1.pos_valida(izquierda) and mapa[izquierda] == buscar:
        found = True
    elif V1.pos_valida(arriba) and mapa[arriba] == buscar:
        found = True
    elif V1.pos_valida(abajo) and mapa[abajo] == buscar:
        found = True
    #Si no está en la salida, modifico el mapa y llamo a la función recursivamente hasta encontrar la salida
    if found == False:
        m_derecha = deepcopy(mapa)
        m_izquierda = deepcopy(mapa)
        m_arriba = deepcopy(mapa)
        m_abajo = deepcopy(mapa)
        m_derecha[derecha] = 4
        m_derecha[pos_jugador] = 0
        if V1.pos_valida(derecha) and mapa[derecha] != 2 and mapa[derecha] != evitar:
            m_derecha[derecha] = 4
            m_derecha[pos_jugador] = 0
            found = existe_solucion(m_derecha, buscar, evitar)
        if not found:
            if V1.pos_valida(izquierda) and mapa[izquierda] != 2 and mapa[izquierda] != evitar:
                m_izquierda[izquierda] = 4
                m_izquierda[pos_jugador] = 0
                found = existe_solucion(m_izquierda, buscar, evitar)
        if not found:
            if V1.pos_valida(arriba) and mapa[arriba] != 2 and mapa[arriba] != evitar:
                m_arriba[arriba] = 4
                m_arriba[pos_jugador] = 0
                found = existe_solucion(m_arriba, buscar, evitar)
        if not found:
            if V1.pos_valida(abajo) and mapa[abajo] != 2 and mapa[abajo] != evitar:
                m_abajo[abajo] = 4
                m_abajo[pos_jugador] = 0
                found = existe_solucion(m_abajo, buscar, evitar)
    return found

#Función para imprimir las sensaciones por pantalla
def imprimir_sensaciones(sensaciones):
    if len(sensaciones) == 0:
        sensaciones.append("No sientes nada")
    print()
    for sensacion in sensaciones:
        print(f" - {sensacion}")
    print()

#Función para ejecutar la partida
def ejecucion_principal(mapa, modo):
    #Modos sin probabilidades
    if modo == 1 or modo == 2:
        #creo array de sensaciones de la misma dimension que el mapa
        mapa_sensaciones = np.zeros((5,5), dtype=object)
        #Creo la base de conocimientos, se que en la casilla 4,0 no hay nada
        kb = [{"D": [(4,0), False]}, {"S": [(4,0), False]}, {"A": [(4,0), False]}]
    #Modos con probabilidades
    else:
        mapa_sensaciones = V2.crear_mapa_Sensaciones(mapa)
        kb = V2.KB_probabilistica()
    estado = None
    disparos = 1
    demogorgon_killed = False
    n_salida = 3 #El número que representa la salida en cada momento del juego ya que puede variar
    #Inicio el bucle del juego
    #El modo Fácil es el modo con certeza absoluta con ayuda y con lógica automática
    #El modo Normal es el modo con certeza absoluta sin ayudas
    if modo == 1 or modo == 2:
        estado = ejecutar_juego_normal(mapa, modo, mapa_sensaciones, kb, estado, disparos, demogorgon_killed, n_salida)
    else:
        estado = ejecutar_juego_probabilistico(mapa, modo, mapa_sensaciones, kb, estado, disparos, demogorgon_killed, n_salida)

    if estado == "Win":
        win_screen()
    elif estado == "Neutral":
        neutral_screen()
    else:
        lose_screen()

#Ejecuto el juego en modo normal, sin probabilidades
def ejecutar_juego_normal(mapa, modo, mapa_sensaciones, kb, estado, disparos, demogorgon_killed, n_salida):
    #Bucle hasta acabar la partida
    while (estado != "Win" or demogorgon_killed == False) and estado != "Lose" and estado != "Demogorgon" and estado != "Salir":
        #Limpio la consola
        clear_console()
        #Imprimo el mapa de juego
        grafico_mapa = V1.imprimir_mapa(mapa, n_salida)
        #Siento
        sensaciones = V1.sentir(mapa, n_salida)
        pos_jugador = (0,0)
        for i in range(5):
            for j in range(5):
                if mapa[i,j] == 4:
                    pos_jugador = (i,j)

        if estado != "Demogorgon" and estado != "Lose":
            imprimir_sensaciones(sensaciones)
        #Actualizo el mapa de sensaciones y lo imprimo
        mapa_sensaciones[pos_jugador] = V1.sensaciones_simplificar(sensaciones)
        grafico_sensaciones = V1.imprimir_tabla_Sensaciones(mapa, mapa_sensaciones)
        #Si hay agente lógico, actualizo la base de conocimientos y recomiendo movimiento
        if modo == 1:
            kb = V1.rellenar_base_conocimientos(kb, pos_jugador, sensaciones, estado)
            mapa_logico = V1.imprimir_mapa_logico(kb)
            V1.recomendacion_prox_movimiento(kb, mapa, demogorgon_killed)
        else:
            mapa_logico = "\n"*11
        #Imprimo el estado del juego
        V1.imprimir_estado_juego(grafico_sensaciones, grafico_mapa, mapa_logico)
        #Obtengo el movimiento del jugador y actualizo el mapa
        mapa, estado, kill, n_salida = V1.obtener_nuevo_mapa(mapa, disparos, n_salida)
        #Compruebo si se ha matado al Demogorgon
        if kill != None:
            disparos = 0
            if kill:
                demogorgon_killed = True
                print("Has matado al Demogorgon")
            else:
                print("Has fallado el disparo")
        #Compruebo si se ha ganado o perdido
        if estado == "Win":
            if disparos == 1:
                print("Has encontrado la salida, pero no puedes dejar escapar al Demogorgon!")
            else:
                print("Has conseguido escapar, pero el Demogorgon sigue suelto y volverá a por tí.")
                demogorgon_killed = True
                return "Neutral"
    return estado

#Ejecuto el juego en modo probabilístico
#Funciona igual que el modo normal, pero con las funciones de la versión 2
def ejecutar_juego_probabilistico(mapa, modo, mapa_sensaciones, kb, estado, disparos, demogorgon_killed, n_salida):
    while (estado != "Win" or demogorgon_killed == False) and estado != "Lose" and estado != "Demogorgon" and estado != "Salir":
        clear_console()
        grafico_mapa = V1.imprimir_mapa(mapa, n_salida)
        sensaciones = V2.sentir(mapa, mapa_sensaciones)
        pos_jugador = (0,0)
        for i in range(5):
            for j in range(5):
                if mapa[i,j] == 4:
                    pos_jugador = (i,j)
        if estado != "Demogorgon" and estado != "Lose":
            imprimir_sensaciones(sensaciones)
        if modo == 3:
            V2.rellenar_base_conocimientos(kb, pos_jugador, mapa_sensaciones, mapa, estado)
            mapa_logico = V2.imprimir_mapa_logico(kb)
            V2.recomendacion_prox_movimiento(kb, demogorgon_killed, mapa)
        else:
            mapa_logico = "\n"*11

        grafico_sensaciones = V2.imprimir_tabla_Sensaciones(mapa, mapa_sensaciones)
        V2.imprimir_estado_juego(grafico_sensaciones, grafico_mapa, mapa_logico)

        mapa, estado, kill, n_salida = V1.obtener_nuevo_mapa(mapa, disparos, n_salida)
        if kill != None:
            disparos = 0
            if kill:
                acierto = V2.obtener_Pr()
                if acierto:
                    demogorgon_killed = True
                    print("Has matado al Demogorgon")
                else:
                    estado = "Demogorgon"
                    print("La bala se ha encasquillado!")
                    print("El Demogorgon te ha visto y ha acabado contigo")
            else:
                print("Has fallado el disparo")
                demogorgon_killed = "Impossible"
        if estado == "Win":
            if disparos == 1:
                print("Has encontrado la salida, pero no puedes dejar escapar al Demogorgon!")
            else:
                print("Has conseguido escapar, pero el Demogorgon sigue suelto y volverá a por tí.")
                demogorgon_killed = True
                return "Neutral"
    return estado

#Bucle principal del juego
if __name__ == "__main__":
    modo = 0
    #Mientras no se elija salir, se ejecuta el juego
    while modo != 5:
        #Imprimo el menú principal y pido la elección del usuario
        imprimir_menu_principal()
        modo = int(pedir_entrada("Introduce tu eleccion: ", ["1", "2", "3", "4", "5", "1.", "2.", "3.", "4.", "5."]))
        if modo != 5:
            #Creo el mapa e inicializo las variables necesarias para el juego
            mapa_ok = False
            while not mapa_ok:
                #A veces al no tener solucion o casos raros puede dar excepciones, por lo que creamos otro
                try:
                    mapa = crear_mapa()
                    mapa_ok = True
                except:
                    pass
            #El modo 1 y 2 corresponden con la versión 1 del juego y los modos 3 y 4 a la versión con probabilidades
            #Imprimo la historia del juego antes de iniciar la partida
            imprimir_historia(modo)
            ejecucion_principal(mapa, modo)

    print("¡Gracias por jugar!")
    print("Saliendo...")
    sys.exit(0)