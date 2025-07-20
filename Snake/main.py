import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from math import sin, cos, pi, sqrt
import time
import random
import re

# Inicializa o pygame
pygame.init()

# Configura a janela
largura, altura = 800, 600
pygame.display.set_mode((largura, altura), DOUBLEBUF | OPENGL)
pygame.display.set_caption("Snake")

# Sistema de coordenadas OpenGL
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
glOrtho(0, largura, altura, 0, -1, 1)
glClearColor(0.8588, 0.8941, 0.6627, 1.0) #cor de fundo

# Classe para segmentos da cobra
class Segmento:
    def __init__(self, x, y, raio=6):
        self.x = x
        self.y = y
        self.raio = raio

# Classe para a cobra controlada por teclas
class Cobra:
    def __init__(self):
        self.segmentos = [Segmento(400, 300, 10)] + [Segmento(400 - i * 10, 300) for i in range(1, 4)]
        self.direcao = (10, 0)
        self.score = 0
        self.crescer_prox = False
        self.ativa = True

    def mover(self):
        if not self.ativa:
            return
        dx, dy = self.direcao
        cabeca = self.segmentos[0]
        nova_x = cabeca.x + dx
        nova_y = cabeca.y + dy
        if nova_x < 0: # Saiu pela esquerda
            nova_x = largura - 10 # Reaparece na direita
        elif nova_x >= largura: # Saiu pela direita
            nova_x = 0 # Reaparece na esquerda
        if nova_y < 0: # Saiu por cima
            nova_y = altura - 10 # Reaparece por baixo
        elif nova_y >= altura: # Saiu por baixo
            nova_y = 0 # Reaparece por cima

        self.segmentos.insert(0, Segmento(nova_x, nova_y, 10))
        if not self.crescer_prox:
            self.segmentos.pop()
        else:
            self.crescer_prox = False

    def crescer(self):
        self.crescer_prox = True
        self.score += 1

    def desenhar(self):
        for i, seg in enumerate(self.segmentos):
            glColor3f(0, 0.6, 0.2) if i > 0 else glColor3f(0.1, 0.8, 0.1)
            desenhar_circulo(seg.x, seg.y, seg.raio)

# Classe para os alvos que seguem trajetórias do Paths_D.txt
class Alvo:
    def __init__(self, caminho):
        self.raio = 6
        self.caminho = caminho
        self.frame_atual = 0
        self.ativo = True
        self.x = 0
        self.y = 0

    def mover(self):
        if self.ativo and self.frame_atual < len(self.caminho):
            self.x, self.y = self.caminho[self.frame_atual]
            self.frame_atual += 1
        else:
            self.ativo = False

    def desenhar(self):
        if self.ativo:
            glColor3f(1.0, 0.0, 0.0)
            desenhar_circulo(self.x, self.y, self.raio)

def desenhar_circulo(x, y, raio):
    glBegin(GL_POLYGON)
    for i in range(30):
        ang = i * (2 * pi / 30)
        glVertex2f(x + raio * cos(ang), y + raio * sin(ang))
    glEnd()

def colidiu(cabeca, alvo):
    dist = sqrt((cabeca.x - alvo.x) ** 2 + (cabeca.y - alvo.y) ** 2)
    return dist < cabeca.raio + alvo.raio

def carregar_alvos(arquivo):
    with open(arquivo, "r", encoding="utf-8") as f:
        linhas = f.readlines()
    escala_match = re.search(r'\[(\d+)\]', linhas[0])
    escala = int(escala_match.group(1)) if escala_match else 1

    max_x, max_y = 1, 1
    caminhos_brutos = []

    for linha in linhas[1:]:
        coords = re.findall(r'\((\d+),(\d+),(\d+)\)', linha)
        if coords:
            caminho = [(int(x), int(y)) for x, y, _ in coords]
            caminhos_brutos.append(caminho)
            for x, y in caminho:
                max_x = max(max_x, x)
                max_y = max(max_y, y)

    fator_x = largura / (max_x / escala)
    fator_y = altura / (max_y / escala)
    fator_escala = min(fator_x, fator_y)

    alvos = []
    for caminho in caminhos_brutos:
        caminho_normalizado = [((x / escala) * fator_escala, (y / escala) * fator_escala) for x, y in caminho]
        alvos.append(Alvo(caminho_normalizado))
    return alvos

cobra = Cobra()
alvos = carregar_alvos("Paths_D.txt")
clock = pygame.time.Clock()
running = True
fim_dos_frames = False
score_impresso = False

while running:
    for evento in pygame.event.get():
        if evento.type == QUIT:
            running = False
        elif evento.type == KEYDOWN:
            if cobra.ativa:
                if evento.key == K_LEFT: cobra.direcao = (-10, 0)
                elif evento.key == K_RIGHT: cobra.direcao = (10, 0)
                elif evento.key == K_UP: cobra.direcao = (0, -10)
                elif evento.key == K_DOWN: cobra.direcao = (0, 10)

    glClear(GL_COLOR_BUFFER_BIT)

    if cobra.ativa:
        cobra.mover()
    cobra.desenhar()

    ativos_restantes = False
    for alvo in alvos:
        alvo.mover()
        alvo.desenhar()
        if alvo.ativo:
            ativos_restantes = True
        if alvo.ativo and colidiu(cobra.segmentos[0], alvo):
            cobra.crescer()
            alvo.ativo = False

    if not ativos_restantes:
        cobra.ativa = False
        if not score_impresso:
            print("SNAKE GAME")
            print(f"Seu SCORE: {cobra.score}")
            score_impresso = True

    pygame.display.flip()
    clock.tick(15)

pygame.quit()
