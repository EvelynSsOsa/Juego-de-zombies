import pygame
import random
import math ## esta libreria la utilizo para poder calcular la distancia que hay entre un obejto y
from pygame import mixer

pygame.init() ## aqui vamos a inicializar a pygame, vamos a traer todas sus herraminetas

### largo = 1200
##ancho = 700
pantalla = pygame.display.set_mode((1200, 700))
## en la variable pantalla, madamos a llamar al metodo "display" de la libreria "pygame", y lo ponemos en ".set_mode"
## este nos ayuda a indicar de que tamaño queremos el display y lo estblecemos dentro de una tupla
fondo = pygame.image.load("fondo.png")
fondo = pygame.transform.scale(fondo,(1200,700))


mixer.music.load('musiquita.mp3')
mixer.music.set_volume(0.4)
mixer.music.play(-1)

pygame.display.set_caption("Invasion Zombie") ## este va a ser el nombre que tenga nuestra ventana, es como el titulo
icono = pygame.image.load("zombie.png") ## en la variable icono mandamos a llamar al metodo "load" de la libreria "pygame" y psamos como parametro el nombre
## de nuestra imagen que cargamos antes al archivo del juego, ahora en esta linea apenas cargamos la imagen al codigo... pero aún no lo establecemos como icono
pygame.display.set_icon(icono)## aquí ya por medio del metodo "display.set_icon" pasamos como parametro la variable icono donde antes cargamos nuestra imagen
## y ahora si ya tenemos un icono establecido


#######################################
####AQUI TENEMOS AL TANQUE(JUAGDOR) JUNTO CON SUS POSISCIONES Y SU IMAGEN
#######################################
img_jugador = pygame.image.load("tank.png") ## cragamos la imagen, de lo sera nuestro disparador
jugador_x = 1136## inicializamos los ejes de las cordenadas en x & y
jugador_y = 500
jugador_y_cambio = 0  ## esta variable nos va ayudar a saber como cambia la posición de nuestro tanque, en el eje de las y
jugador_x_cambio = 0 ## esta variable nos va ayudar a saber como cambia la posición de nuestro tanque, en el eje de las x
## como estas 2 se van a ir actualizndo cada que el ususario decida apretar una tecla, se inicializan en 0

###### tenemos que la imagen del tanque y el enemigo es de 64, entonces si mi largo es de 800, le resto 64 y me queda 736....
# colocamos a una distancia que nos agrade de inicio como referencia para el eje x
##### tenemos a 600 de ancho, y le restamos 64, lo que quiere decir que nos queda 536...
# y si lo queremos a la mitad, dividimos a 536/2 nos da 268

#####################################
###AQUÍ TENEMOS AL ENEMIGO QUE, JUNTO CON SUS MOVIMENTOS Y SU IMAGEN
####################################
game_over = False
## para poder rcear varios zombies / enemigos al mismo tiempo
## vamosa crear diferentes listas, con las diferentes poisciones de nuestros zoombies
img_enemigo = [] ## aqui vamos a crear una lista que contenga 8 veces la imagen del zombie
enemigo_x = [] ## aqui 8 posisciones en x para nuestro zombie
enemigo_y = [] ## aquí 8 posiciones en y para nuestro zombie
enemigo_x_cambio = [] ## aquí vamos a ir colocando las cordenadas de cambio en x de nuestro zombie
enemigo_y_cambio = []## aquí vamos a ir colocando las cordenadas de cambio en y  de nuestro zombie
cantidad_enemigos = 8 ## aqui solo decimos cuantos zombies vamos a ir generando, siempre habra 8 zombies

for e in range (cantidad_enemigos):## decimos que por cada elemento de nuestro rango de 8, iremos agregamos a cada una de las siguientes listas:
    img_enemigo.append(pygame.image.load("enemigo.png"))## cargamos la imagen, de lo seran nuestros enemigos
    ##como el enemigo se tiene que mover solito por medio del metodo "random.randint" le pasamos las cordenads en eje x & y
    enemigo_x.append(random.randint(0,1136))##entonces en eje x de 1200 -64 bits del enemigo, nos queda del punto 0 al 1136
    enemigo_y.append(random.randint(500,630))##entonces en eje y de 500 a 630
    ##para que quede noun pequeño espacio antes le vamos a dar 20 puntos
    enemigo_x_cambio.append(0.3) ## esta variable nos va ayudar a saber como cambia la posición de nuestro enemigo
    enemigo_y_cambio.append(0.3) ## antes 50


######################################
######AQUÍ TENEMOS LAS MUNICIONES QUE VAN A SER UN OSITO DE PELUCHE
######################################
img_bala = pygame.image.load("osito.png") ## cargamos la imagen, que ahora va ser lo que usaremos como bala
#bala_x = 1136 ## nosotros vamos a disparar de forma horizontal por eso colocamos a la bala en x
#bala_y = 0 ### "bala_y" empieza en 0, pero cuando disparo toma la posición del jugador
bala_x_cambio = 2 ## supongo que esta sera la velocidad de la bala en x
#bala_y_cambio = 0 ## aqui nunca habra en cambio en esta posisción por eso se inicializa en 0, LA DOCUMENTO
#bala_visible = False ## a bala_visible la vamos a inicializar en False porque esta no queremos que se vea hasta que sea presionada la tecla espaciadora
balas = []


##### Voy a cargar la imagen de corazones para el juego
corazon_img = pygame.image.load("cora.png")
img_corazon = pygame.transform.scale(corazon_img,(32,32))

vidas = 3 ## esamos son las vidas default/ oprtunidades que tenemos antes de que lo enemigos nos alcencen
puntaje = 0
fuente = pygame.font.Font('LeslieCrayon-Bold.ttf',32)
texto_x = 10
texto_y = 10
## texto final
fuente_final = pygame.font.Font('LeslieCrayon-Bold.ttf',40)

#esta función de aqui nadamas me ayuda a sacar el texto final cuando termina el juego
def texto_final():
    mi_fuente_final = fuente_final.render("GAME OVER", True,(255,255,255))
    pantalla.blit(mi_fuente_final,(60,200))

## ahora tenemos una función que me ayuda a mostrar cuantas vidas tenemos al usuario:
def mostrar_vidas(x,y):
    for i in range(vidas):
        pantalla.blit(img_corazon,(x + i * 40, y))
def mostrar_puntaje(x,y):
    texto = fuente.render(f'Puntaje: {puntaje}', True, (255,255,255))
    pantalla.blit(texto,(x,y))
def jugador (x,y):## luego creamos un funcón que nos va a ayudar a arrojar al jugador en pantalla
    pantalla.blit(img_jugador, (x,y))
    ## madamos a llamar a nuestra pantalla y por medio del metodo "blit", pasamos la imagen del "disparador/jugador/tanque"
    # y las cordenadas que pasamos como paremtro antes, esto nos va a permitir que se puedan dar distintas cordenadas

def enemigo(x,y, ene):## luego creamos un funcón que nos va a ayudar a arrojar al jugador en pantalla
    pantalla.blit(img_enemigo[ene], (x,y))
    ## madamos a llamar a nuestra pantalla y por medio del metodo "blit", pasamos la imagen del "disparador/jugador/tanque"
    # y las cordenadas que pasamos como paremtro antes, esto nos va a permitir que se puedan dar distintas cordenadas

###############################################
###LOGICA PARA UNA SOLA BALA
## creamos una función para poder mostrar la bala en pantalla
#def disparar_bala(x,y): ## pasamos los parametros de la posisción de la bala
     #global bala_visible ## madamos allamar a la variable global "bala_visible"
     #bala_visible = True ## y ke cambiamos el valor a "True"
     #pantalla.blit(img_bala,(x,y)) ## ahora por medio del metodo "blit" pasamos la imagen y las 2 variables que son sus
     ## posisciones
######################################################


 ## aqui voy a detectar colicciones....para poder calcular la distancia, exite una formula
 ## d = √(x1-x2)^2 + (y1-y2)^2 -> Con ayuda de esta formula podemos obtener cuantos pixeles de distancia tenemos entre el enemigo y la bala
def detectar_colision(x_1,y_1,x_2,y_2):## se pasan las pisbles posisciones en x & y de los 2 objetos a los que les queremos sacar la distancia
    distancia = math.sqrt(math.pow(x_1 - x_2,2)+ math.pow(y_1 - y_2,2))
    ## en la variable "distancia" vamos a guardar los el resultado
    ## importante recordar que el metodo "math.sqrt" -> nos ayuda a sacar la raiz cuadrada de un valor
    ## y que el metodo "math.pow", nos ayuda a obtener el cuadrado
    if distancia < 27: ## decimos que si la distancia obtenida entre nuestro objeto uno y el objeto 2 es menos a 27 pixeles
        return True## regresemos True, es decir "que hubo colicción", pero aun no lo marcamos como colisisón
    else: ## en dado caso de que haya mas de 27 pixeles dde distancia entre un objeto y otro
        return False ## nos va a regresar "False" es decir que no hay colisón entre obj1 y obj2

se_ejecuta = True ## en la variable "se_ejecuta" guardamos un boooleano
while se_ejecuta: ## decimos que miestra "se_ejecuta" tenga valor "True", entonces vamos a hacer, queee....  ********

    #pantalla.fill((125, 100, 17))  ## aquí establecemos el color de la pantalla
    pantalla.blit(fondo,(0,0))

    for evento in pygame.event.get():## que por cada evento, dentro de "pygame.event.get()" *********
        if evento.type == pygame.QUIT:## si vemos que el tipo de un evento es igual a "pygame.QUIT"
            se_ejecuta = False## entonces la variable "se_ejecuta", pasa a ser "False"

        if evento.type == pygame.KEYDOWN: ### aquí tenemos un evento donde, verificamos si una tecla fue presionada, no importa cual sea
            if evento.key == pygame.K_LEFT: ## decimos que si se presiona la felcha izquierda
                jugador_x_cambio = -0.3 ### vamos a establecer a "jugador_x_cambio" en "-0.3" que nos indica la velocidad con la que vamos a avanzar
                ## es decir que si vamos a la izquierda restamos
                print("Flecha izquierda presionada")## esto se imprime en pantalla cada vez que la tecla izquieerda se presiona
            if evento.key == pygame.K_RIGHT: ## ahora decimos que en dado caso de que la tecla presinada sea la derecha
                jugador_x_cambio = 0.3 ## vamos a establecer a "jugador_x_cambio" en "0.3", como vamos a la derecha sumamos
                print("Flecha derecha presionada") ## esto se imprime en pantalla cada vez que la tecla derecha es presionada
            if evento.key == pygame.K_UP:## aqui tambien coloque las flechas de arriba y de abajo
                jugador_y_cambio = -0.3 ## cuando va hacia arriba aumenta
                print("Flecha hacia arriba presionda")
            if evento.key == pygame.K_DOWN:
                jugador_y_cambio = 0.3
            if evento.key == pygame.K_SPACE: ## decimos que si se presiona la barra espaciadora verifcaremos si:
                sonido_bala = mixer.Sound('disparo.wav')
                sonido_bala.play()
                balas.append([jugador_x, jugador_y + 20])
                ######ESTA ERA LA LOGICA PARA QUE SOLO SE VIERA UNA BALA/OSITO A LA VEZ

                # if not bala_visible: ## si la variable global de "bala_visible" no tiene un valor "TRUE" es decir "FALSE"
                    # bala_x = jugador_x## "bala_x" tendra la misma posisción que la del jugador(esto dependiendo a donde se haya movido)
                    # bala_y = jugador_y + 20# "bala_y" sera iguala a la posisción que tiene en y el jugador, mas otros 20 pixeles
                    # bala_visible = True## a bala visible le vamos a cambiar su valor a true

                #########################################################################
### hay un momento  donde el usuario va a dejar de presionar la flecha entonces ahí
        if evento.type == pygame.KEYUP:## se elevan las teclas, ya sea la izquierda o la derecha
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0 ## a jugador cambio lo vamos a establecer en 0, en su nueva posisción donde haya quedado cuando el usuario dejo
                #de presinar la tecla
                print("La fecha fue soltada") ## y esto va a ser lo que vamos a imprimir en pantalla
            if evento.key == pygame.K_UP or evento.key == pygame.K_DOWN: ## y hacemos lo mismo para las teclas de arriba de abajo
                jugador_y_cambio = 0
                print("La fecha fue soltada")  ## y esto va a ser lo que vamos a imprimir en pantalla

###########################################
############### AQUÍ PONEMOS LOS MOVIMIENTOS LIMITE DEL JUGADOR(TANQUE)
###########################################
    jugador_x += jugador_x_cambio
    jugador_y += jugador_y_cambio
    ## Aquí fue necesario poder establecer los valores maximos del movimeinto del tanque en el eje y:
    ##tomando en cuenta qu ele pixel 0 empeiza en lo alto de la pnatalla y el pixel 700 hasta abajo, y restando el tamaño del tanque
    ##64 bits, nos deje un espacio de 636 pixeles para movernos,
    y_max = 500 ## 500 pixeles es la altura maxima que puede alcanzar nuestro tanque, no más si no quedaría flotando en el cielo
    y_min= 636 ## 636 pixeles son la profundidad minima a la que queremos que llegue nuestro tanque sin salir de la pantalla

    if jugador_x <= 0: ## si el "jugador_x", se encuentra en la posición menor a 0 o igual a 0, es decir en el eje de las x:
        jugador_x = 0 ## entonces el jugador tendra un cordenada equivalente a  0, siempre y cuando se cumpla la condición de arriba
        ## esto lo que provoca es que, no podemos pasar del liminte de la pantalla, ya que llegando a cierta cordenada, el valor siempre sera 0
    ### CUANDO DECIMOS QUE SI "jugador_x" es mayor o igual a 1136(1200-64bits de personje), hablamos de avanzar hacia el lado derecho y sus limites:
    if jugador_x >= 1136: ## cuando "jugador_x" se encuentre en una cordenada mayor o igual 1136...
        jugador_x = 1136## su valor de cordenada siempre se mantendra en 736... no hay escapatoria

    ## esto tambien lo coloque porque quiero que mi jugador se pueda mover hacia arriba y hacia abajo, en el area del pasto de la imagen
    if jugador_y <= y_max: ## decimos que si "jugador_y" se encunetra en una posición menor o igual a "y_max" que es la altura maxima que puede alcanzar el tanque
        jugador_y = y_max ## entonces al tomar esa cordenada, su valor no puede aumentar

    if jugador_y >= y_min: ## decimos que si "jugador_y" se encuentra en una posición mayor a 636... lo mas profundo de la pantalla
        jugador_y = y_min## "jugador_y", va a tomar el valor de las cordenadas 636 y no podra cambiar su valor, provocando que no pueda salir de pantalla



#################################################

#######AQUí VAMOS A PONER EL MOVIMIENTO LIMITE  DEL ENEMIGO########
    ## se coloca un indice "[e]" que nos indicare el numero de zombie que es un nustro rango de 8

#################################################

        ### entonces aun dentro del ciclo for, vamos a decir que se le agregue la nueva posión que quedo en "enemigo_x_cambio" (esto es solo para x )
    if not game_over:
        for e in range(cantidad_enemigos):
            enemigo_x[e] += enemigo_x_cambio[e]  ## aqui vamos a ir sumando el movimiento en x a la posición actual del enemigo

            if enemigo_x[e] >= 1136: ## enteonces decimos que si el enemigo estando en el eje x, toma una cordenada  mayor a "1136" pixel:
                vidas -= 1 ## le restamos una vida (recuerda tenemos 3)
                ## reiniciamos a ese zombie/enemigo:
                enemigo_x[e] = random.randint(0, 1136)  ##entonces en eje x de 1200 -64 bits del enemigo, nos queda del punto 0 al 1136
                enemigo_y[e] = random.randint(500, 630)  ##entonces en eje y de 500 a 630
                ## decimos que si vidas es menor a 0 o igual, entonces:
                if vidas <= 0:
                    game_over = True
                    break

                # SI SALE POR LA IZQUIERDA (solo respawn)
            if enemigo_x[e] <= 0:
                enemigo_x[e] = random.randint(0, 1136)
                enemigo_y[e] = random.randint(500, 630)

            #### Aquí vamos a ponerle limites a nuestro tanque, porque no queremos que salga de la pantalla, para ello, entonces decimos que

            ####Cunado decimos que si el jugador es menor o igual a 0 -> unicamente nos referimos al lado izquierdo

            if enemigo_y[e] <= 500:  ## si el "enemigo_x", se encuentra en la posición menor a 0 o igual a 0, es decir en el eje de las x:
                enemigo_y[e] = 500
                enemigo_y_cambio[e] = 0.3 ## entonces el jugador tendra un cordenada equivalente a  0, siempre y cuando se cumpla la condición de arriba
                ## esto lo que provoca es que, no podemos pasar del liminte de la pantalla, ya que llegando a cierta cordenada, el valor siempre sera 0
            ### CUANDO DECIMOS QUE SI "jugador_x" es mayor o igual a 736(800-64bits de personje), hablamos de avanzar hacia el lado derecho y sus limites:
            #enemigo_x[e]+= enemigo_x_cambio[e]  ahorita lo regreso por si no me sale me da miedo

            if enemigo_y[e] >= 630: ## cuando "jugador_x" se encuentre en una cordenada mayor o igual 630...
                enemigo_y[e] = 630## su valor de cordenada siempre se mantendra en 736... no hay escapatoria
                enemigo_y_cambio[e] = -0.3
                #enemigo_x[e]  += enemigo_x_cambio[e]

            ## enteonces en la variable "colision" vamos a mandar a llamar a la función "detectar_colision"
            ## y le pasamos los paramteros entre los 2 objetos que quremos saber si chocaran o no,
            ## es importante recordar que si están a menos de 27 pixeles de distancia -> hay colision, si se encuentran a más de 27 pixeles -> no hay colision
            for bala in balas[:]:
                colision = detectar_colision(enemigo_x[e], enemigo_y[e], bala[0], bala[1])
                if colision:  ## decimos que si nuestra función nos devolvio un valor "TRUE"
                    sonido_colision = mixer.Sound('zombie.wav')
                    sonido_colision.play()
                    #bala_y = 500  ## volvamos a restablecer la bala en la posición
                    #bala_visible = False
                    puntaje += 1
                    balas.remove(bala)
                    enemigo_x[e]= random.randint(0,1136)  ##entonces en eje x de 1200 -64 bits del enemigo, nos queda del punto 0 al 1136
                    enemigo_y[e] = random.randint(500, 630)  ##entonces en eje y de 500 a 630
                    break

            enemigo(enemigo_x[e] ,enemigo_y[e], e)
        for bala in balas:
            bala[0] -= bala_x_cambio  # mover en X
            pantalla.blit(img_bala, (bala[0], bala[1]))
        balas = [bala for bala in balas if bala[0] > 0]
#############################################Esta era la logica de cuando solo tenia una bala/osito
        # movimiento de la bala ##########
        ## decimos que si "bala_visible" toma un valor "True"(es decir ya se presiono la tecla de espacio)
        #if bala_visible: ## bala_x, va a ser igual a un decremento de "bala_x_cambio", pues si nuestro tanque dispara del lado derecho de la pantalla
            #bala_x -= bala_x_cambio## es logico que si vamos hacia la izquierda se reste un pixel, para simular movimiento
            #disparar_bala(bala_x, bala_y)## madamos a llamar a la función que nos muestra la bala y pasamos las posiciones de la bala en x & y como
            ## parametro
#########################################################################



    ## aqui ya solo estamos mandado a llamar a la función y le estamos pasando los parametros con los nuevos valores
    jugador(jugador_x,jugador_y)
    mostrar_puntaje(texto_x,texto_y)
    mostrar_vidas(10,80)
    if game_over:
        texto_final()

    pygame.display.update() ## y hacemos actualización de nuestra