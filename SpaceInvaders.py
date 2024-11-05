# -----------------------------------------------------------------------------
# Nombre del Programa: SpaceInvaders.py
# Autor: Fátima Illana Guerra
# Fecha: 3/12/21
# Objetivo del porgrama: Juego Space Invaders. 
# -----------------------------------------------------------------------------

import pygame
import sys
import random
from typing import List
from cinco_máximos import ganadores

# CONSTANTES: 
ANCHO = 720
ALTO = 720
LADO = 100

# COLORES:
ROJO = (255, 0, 0)
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

# Comenzamos pidiendo el nomre del jugador:
nombre_jugador = str(input("Introduzca el nombre del jugador: "))
if nombre_jugador == "":
    nombre_jugador = "Jugador"
    
# Iniciamos funciones de pygame:
pygame.init()
pygame.display.init()
pygame.font.init()
pygame.mixer.init()

# Creamos la ventana:
ventana = pygame.display.set_mode ((ANCHO, ALTO))
pygame.display.set_caption("SPACE INVADERS")
clock = pygame.time.Clock()

# Iniciamos bucles y contador:
finalizado = False
menu_cerrado = False
nivel_seleccionado = True
cerrar_info = True
inicio = True
game_over = True 
salir = True
contador = 0

# Tipografía:
fuente_retro = "prstart.ttf"

# Música y Sonidos:
pygame.mixer.music.load("musica_fondo.wav")
pygame.mixer.music.set_volume(0.5)
laser_sonido = pygame.mixer.Sound("laser.ogg")
muerte_sonido = pygame.mixer.Sound("muerte.wav")
boton_pulsado_sonido = pygame.mixer.Sound("boton_pulsado.wav")

# IMÁGENES:
imagen_fondo = pygame.image.load("background.png").convert()
inicio = pygame.image.load("start-button_opt.png").convert()
salida = pygame.image.load("exit_opt.png").convert()
nivel1 = pygame.image.load("numero-1_opt.png").convert()
nivel2 = pygame.image.load("numero-2_opt.png").convert()
nivel3 = pygame.image.load("numero-3_opt.png").convert()
instrucciones = pygame.image.load("informacion_opt.png").convert()
volver = pygame.image.load("volver_opt.png").convert()

# Creamos listas de sprites:
lista_enemigos = pygame.sprite.Group()
lista_sprites = pygame.sprite.Group()
lista_disparos = pygame.sprite.Group()
        
# CLASES:
class Botón ():
    def __init__(self, x, y, image):
        self.image = image
        self.image.set_colorkey(NEGRO)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def mostrar (self):
        ventana.blit(self.image, self.rect)
    def pulsado(self):
        pulsado = False
        posicion = pygame.mouse.get_pos()
        if self.rect.collidepoint (posicion):
            if pygame.mouse.get_pressed()[0] == 1:
                boton_pulsado_sonido.play()
                pulsado = True
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        return pulsado

class Barrera (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((720, 1))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 720
    def mostrar (self):
        ventana.blit(self.image, self.rect)
    
class Disparo (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((10, 15))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.y = (ALTO - (LADO) * (3 / 2))
    def update (self):
        self.rect.y -= 15
        
class Enemigo(pygame.sprite.Sprite):
    def __init__ (self):
        super().__init__()
        self.image = pygame.image.load("alien11_opt.png").convert()
        self.image.set_colorkey(NEGRO)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, ANCHO - LADO)
        self.rect.y = random.randint(-LADO * 2, -LADO)
    def update(self) -> int:
        self.rect.y += 7
        
class Jugador(pygame.sprite.Sprite):
    def __init__ (self):
        super().__init__()
        self.image = pygame.image.load("nave_retro.png").convert()
        self.image.set_colorkey(NEGRO)
        self.rect = self.image.get_rect()
        self.rect.y = ALTO - LADO * (3/2)
        self.rect.x = ANCHO / 2 - LADO
    def update (self):
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            if (self.rect.x <= 0):
                self.rect.x = 0
            else:
                self.rect.x -= 30
        elif keystate[pygame.K_RIGHT]:
            if (self.rect.x >= ANCHO - LADO):
                self.rect.x = (ANCHO - LADO)
            else:
                self.rect.x += 30
    def disparar (self):
        laser = Disparo ()
        laser.rect.x = (self.rect.x + (LADO / 2))
        lista_sprites.add(laser)
        lista_disparos.add(laser)
        laser_sonido.play()

# FUNCIONES:
def crear_texto (superficie, texto, fuente, tamaño, color, x, y) -> None:
# """Crea un texto y lo dibuja en la ventana."""
    fuente = pygame.font.Font(fuente, tamaño)
    texto = fuente.render(texto, True, color)
    texto_rect = texto.get_rect()
    texto_rect.x = x
    texto_rect.y = y
    superficie.blit(texto, texto_rect)

def imprimir_fichero (archivo : str) -> None:
# """Imprime en pantalla, el contenido de un archivo."""
    fichero = open(archivo)
    linea = fichero.readline()
    distancia = 50
    while linea != "":
        crear_texto(ventana, linea.rstrip(), fuente_retro, 20, BLANCO, 0, distancia)
        distancia += 50
        linea = fichero.readline()
    fichero.close()

def colisiones_sprite_enemigo(sprite, lista_enemigos) -> bool:
# """Detecta las colisiones entre el jugador/barrera y los enemigos."""
    return pygame.sprite.spritecollide(sprite, lista_enemigos, True)

def colisiones_disparo_enemigo (lista_disparos, lista_enemigos) -> bool:
# """Detecta las colisiones entre los disparos y los enemigos."""
    return pygame.sprite.groupcollide(lista_disparos, lista_enemigos, True, True, collided = None)

def crear_enemigos (n : int) -> None:
# """Crea un número n de enemigos."""
    for i in range (n):
        enemigo = Enemigo()
        lista_enemigos.add(enemigo)
        lista_sprites.add(enemigo)

# CONSTRUCTOR:
  # Creamos enemigos:
crear_enemigos(6)
  # Creamos al jugador:
player = Jugador()
lista_sprites.add(player) 
 # Creamos la barrera:
barrera = Barrera()
  # Creamos los botones:
inicio_bot = Botón (216, 200, inicio)
salida_bot = Botón (308, 400, salida)
nivel1_bot = Botón (50, 243, nivel1)
nivel2_bot = Botón (260, 243, nivel2)
nivel3_bot = Botón (470, 243, nivel3)
instrucciones_bot = Botón (620, 620, instrucciones)
volver_bot = Botón (10, 620, volver)

# JUEGO:
while not finalizado:
    
    # PANTALLA INICIO
    while not menu_cerrado: 
        ventana.blit(imagen_fondo, [0, 0]) 
        crear_texto(ventana, "SPACE INVADERS", fuente_retro, 50, BLANCO, 15, 100)
        inicio_bot.mostrar()
        salida_bot.mostrar()
        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or (salida_bot.pulsado()):
                sys.exit()
                finalizado = True
            if inicio_bot.pulsado():
                menu_cerrado = True
                nivel_seleccionado = False
        pygame.display.update()
    
    # PANTALLA INSTRUCCIONES:
    while not cerrar_info:
        ventana.blit(imagen_fondo, [0, 0]) 
        volver_bot.mostrar()
        imprimir_fichero("instrucciones.txt")
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                sys.exit()
                Finalizado = True
            elif volver_bot.pulsado():
                nivel_seleccionado = False
                cerrar_info = True
        pygame.display.update()
    
    # PANTALLA NIVELES
    while not nivel_seleccionado:
        ventana.blit(imagen_fondo, [0, 0]) 
        crear_texto(ventana, "NIVELES", fuente_retro, 50, BLANCO, 200, 100)
        pygame.mixer.music.play(-1)
        nivel1_bot.mostrar()
        nivel2_bot.mostrar()
        nivel3_bot.mostrar()
        instrucciones_bot.mostrar()
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                sys.exit()
                Finalizado = True
            elif nivel1_bot.pulsado():
                nivel_seleccionado = True
                game_over = False
                frames_segundo = 30
            elif nivel2_bot.pulsado():
                nivel_seleccionado = True
                game_over = False
                frames_segundo = 40
            elif nivel3_bot.pulsado():
                nivel_seleccionado = True
                game_over = False
                frames_segundo = 50
            elif instrucciones_bot.pulsado():
                nivel_seleccionado = True
                cerrar_info = False
        pygame.display.update()
    
    # PANTALLA INSTRUCCIONES:
    while not cerrar_info:
        ventana.blit(imagen_fondo, [0, 0]) 
        pygame.mixer.music.stop()
        volver_bot.mostrar()
        imprimir_fichero("instrucciones.txt")
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                sys.exit()
                Finalizado = True
            elif volver_bot.pulsado():
                nivel_seleccionado = False
                cerrar_info = True
        pygame.display.update()
    
    # PANTALLA JUEGO    
    while not game_over:
        ventana.blit(imagen_fondo, [0, 0])      
        crear_texto(ventana, "MARCADOR: " + str(contador), fuente_retro, 30, BLANCO, 5, 5)
        barrera.mostrar()
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                sys.exit()
                Finalizado = True
            elif (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_SPACE):
                    player.disparar()
        lista_sprites.update()
        lista_sprites.draw(ventana)
        if colisiones_sprite_enemigo (player, lista_enemigos):
            game_over = True
            salir = False
            muerte_sonido.play()
            pygame.mixer.music.stop()
        elif colisiones_disparo_enemigo (lista_disparos, lista_enemigos):
            crear_enemigos(1)
            contador += 1
        elif colisiones_sprite_enemigo (barrera, lista_enemigos):
            crear_enemigos(1)
            contador -= 1
        if len(lista_enemigos) <= 4:
            crear_enemigos(4)
        clock.tick(frames_segundo)
        pygame.display.update()
    
    # AÑADIMOS EL CONTADOR AL ARCHIVO DE PUNTUACIONES
    puntuaciones = open("Puntuaciones.txt", "a")
    puntuaciones.write(nombre_jugador + " " + str(contador) + "\n")
    puntuaciones.close()
    lista_puntuaciones : List[int] = ganadores("Puntuaciones.txt")
        
    # PANTALLA GAME_OVER:
    while not salir:
        ventana.fill(NEGRO)
        crear_texto(ventana, "GAME OVER", fuente_retro, 60, BLANCO, 90, 100)
        distancia = 250
        for i in lista_puntuaciones:
            crear_texto(ventana, i[0], fuente_retro, 20, BLANCO, 30, distancia)
            crear_texto(ventana, " --------------->    " + i[1], \
                        fuente_retro, 20, BLANCO, 200, distancia)
            distancia += 60
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                sys.exit()
                Finalizado = True
        pygame.display.update()
pygame.quit()
