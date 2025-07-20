import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from math import sin, cos, pi, sqrt
import time
import random
import re

class Personagem:
    def __init__(self):
        self.x = []
        self.y = []
        self.frame_atual = 0
        self.ativo = True
        self.cor = (random.random(), random.random(), random.random())
        self.raio = 8
        self.vivo = True
        self.controlado = False
        self.pos_x = 0
        self.pos_y = 0

personagens = []
score = 0
fim_dos_frames = False
score_mostrado = False

# Leitura dos dados
def carregar_dados(arquivo):
    global personagens
    personagens = []

    with open(arquivo, "r", encoding="utf-8") as file:
        linhas = file.readlines()

    escala_match = re.search(r'\[(\d+)\]', linhas[0])
    escala = int(escala_match.group(1)) if escala_match else 1

    max_x, max_y = 1, 1

    for linha in linhas[1:]:
        linha = linha.strip()
        if not linha:
            continue

        coords = re.findall(r'\((\d+),(\d+),(\d+)\)', linha)
        if not coords:
            continue

        p = Personagem()
        for x, y, f in coords:
            x, y = int(x), int(y)
            p.x.append(x)
            p.y.append(y)
            max_x = max(max_x, x)
            max_y = max(max_y, y)

        personagens.append(p)

    # Fatores de escala para ajustar à tela
    fator_x = 800 / (max_x / escala)
    fator_y = 600 / (max_y / escala)
    fator_escala = min(fator_x, fator_y) 

    for p in personagens:
        p.x = [(x / escala) * fator_escala for x in p.x]
        p.y = [(y / escala) * fator_escala for y in p.y]

    # Marca o primeiro personagem como controlável
    if personagens:
        personagens[0].controlado = True
        personagens[0].pos_x = personagens[0].x[0]
        personagens[0].pos_y = personagens[0].y[0]

def desenhar_circulo(x, y, raio):
    glBegin(GL_POLYGON)
    for i in range(30):
        ang = i * (2 * pi / 30)
        glVertex2f(x + raio * cos(ang), y + raio * sin(ang))
    glEnd()

def colidiu(px, py, raio, p2):
    if not p2.ativo:
        return False
    x2 = p2.x[p2.frame_atual]
    y2 = p2.y[p2.frame_atual]
    dist = sqrt((px - x2) ** 2 + (py - y2) ** 2)
    return dist < raio + p2.raio

def desenhar_personagens():
    for idx, p in enumerate(personagens):
        if not p.ativo:
            continue
        if p.controlado:
            glColor3f(0.1, 0.6, 0.1)
            desenhar_circulo(p.pos_x, p.pos_y, p.raio)
        elif p.frame_atual < len(p.x):
            glColor3f(*p.cor)
            desenhar_circulo(p.x[p.frame_atual], p.y[p.frame_atual], p.raio)

def main():
    global score, fim_dos_frames, score_mostrado
    pygame.init()
    largura, altura = 800, 600
    # Inicializa a janela OpenGL com buffer duplo para evitar flickering (tremulação na tela)
    pygame.display.set_mode((largura, altura), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Agar.io")

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, largura, altura, 0, -1, 1)
    glClearColor(1.0, 1.0, 1.0, 1.0)

    carregar_dados("Paths_D.txt")
    clock = pygame.time.Clock()

    running = True
    while running:
        for evento in pygame.event.get():
            if evento.type == QUIT:
                running = False

        if personagens:
            p0 = personagens[0]
            if not fim_dos_frames:
                teclas = pygame.key.get_pressed()
                if teclas[K_LEFT]: p0.pos_x -= 3
                if teclas[K_RIGHT]: p0.pos_x += 3
                if teclas[K_UP]: p0.pos_y -= 3
                if teclas[K_DOWN]: p0.pos_y += 3 

                if p0.pos_x - p0.raio < 0: 
                    p0.pos_x = p0.raio 
                elif p0.pos_x + p0.raio > largura: 
                    p0.pos_x = largura - p0.raio 

                if p0.pos_y - p0.raio < 0: 
                    p0.pos_y = p0.raio 
                elif p0.pos_y + p0.raio > altura: 
                    p0.pos_y = altura - p0.raio 

                for i in range(1, len(personagens)):
                    p = personagens[i]
                    if p.ativo and p.frame_atual < len(p.x):
                        if colidiu(p0.pos_x, p0.pos_y, p0.raio, p):
                            p.ativo = False
                            score += 1
                            p0.raio += 1.5

        glClear(GL_COLOR_BUFFER_BIT)

        desenhar_personagens()

        fim_dos_frames = all(p.frame_atual >= len(p.x) - 1 for p in personagens if not p.controlado)

        # Esta verificação garante que a mensagem de SCORE seja exibida apenas uma vez
        if fim_dos_frames and not score_mostrado:
            print("\n========= AGAR.IO =========")
            print(f"Seu SCORE: {score}")
            print("===========================\n")
            score_mostrado = True

        for i, p in enumerate(personagens):
            if not p.controlado and p.frame_atual < len(p.x) - 1:
                p.frame_atual += 1

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
