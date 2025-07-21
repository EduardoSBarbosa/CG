from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from Ponto import *

import math
import random

class Objeto3D:

    def __init__(self):
        self.vertices_original = []
        self.vx = []
        self.vy = []
        self.vz = []
        self.vy_vortex = []

        self.vertices = []
        self.faces    = []
        self.speed    = []
        self.angle    = []
        self.radius   = []
        self.position = Ponto(0,0,0)
        self.rotation = (0,0,0,0)

        self.vortex_offset_angle = 0
        self.vortex_radius = 1.0

        self.direcoes = []
        self.frame_animacao = 0  # para uso em rotação  

        # NOVO ATRIBUTO: Vértices de destino para a forma de esfera
        self.vertices_esfera_destino = []
        self.vertices_esfera_destino = []
        
    def LoadFile(self, file:str):
        f = open(file, "r")
        for line in f:
            values = line.split(' ')
            if values[0] == 'v': 
                x = float(values[1])
                y = float(values[2])
                z = float(values[3])
                v = Ponto(x, y, z)

                self.vertices.append(v)
                self.vertices_original.append(Ponto(x, y, z))

                self.vx.append(random.uniform(-0.1, 0.1))
                self.vy.append(random.uniform(0.1, 0.3))
                self.vz.append(random.uniform(-0.1, 0.1))

                self.speed.append((random.random() + 0.1))
                self.angle.append(math.atan2(z, x))
                self.radius.append(math.hypot(x, z))

                dist = math.hypot(x, z)
                self.vy_vortex.append(0.03 + max(0, 1.5 - dist) * 0.02)
                self.direcoes.append([0.0, 1.0, 0.0])

            if values[0] == 'f':
                self.faces.append([])
                for fVertex in values[1:]:
                    fInfo = fVertex.split('/')
                    self.faces[-1].append(int(fInfo[0]) - 1)
        pass

    def AtualizaFraseFinal(self, alpha):
        for i in range(len(self.vertices)):
            d = self.destino_frase[i % len(self.destino_frase)]
            v = self.vertices[i]
            v.x = (1 - alpha) * v.x + alpha * d.x
            v.y = (1 - alpha) * v.y + alpha * d.y
            v.z = (1 - alpha) * v.z + alpha * d.z

    def AtualizaVortex(self, frame):
        self.frame_animacao = frame
        self.vortex_offset_angle += 0.08

        for i in range(len(self.vertices)):
            v = self.vertices[i]

            dx = v.x
            dz = v.z
            dist = math.hypot(dx, dz)

            angulo = 0.5 + 1.0 / (1 + dist)
            cos_a = math.cos(angulo + self.vortex_offset_angle)
            sin_a = math.sin(angulo + self.vortex_offset_angle)

            x = dx * cos_a + dz * sin_a
            z = -dx * sin_a + dz * cos_a

            v.x = x
            v.z = z

            if dist < 2.0:
                v.y += self.vy_vortex[i]

        # zera a rotação assim que o vórtex termina
        if frame >= 90:
            self.frame_animacao = 0

    def AtualizaEstilhaçamento(self):
        for i in range(len(self.vertices)):
            self.vertices[i].x += self.vx[i]
            self.vertices[i].y += self.vy[i]
            self.vertices[i].z += self.vz[i]
            self.vy[i] -= 0.01

    def DepositaParticulasNoChao(self):
        for i in range(len(self.vertices)):
            if self.vertices[i].y > 0:
                self.vertices[i].x += self.vx[i]
                self.vertices[i].y += self.vy[i]
                self.vertices[i].z += self.vz[i]
                self.vy[i] -= 0.01
            else:
                self.vertices[i].y = 0
                self.vy[i] = 0
                self.vx[i] = 0
                self.vz[i] = 0

    def Reconstrucao(self, alpha):
        for i in range(len(self.vertices)):
            v = self.vertices[i]
            d = self.vertices_original[i]
            v.x = (1 - alpha) * v.x + alpha * d.x
            v.y = (1 - alpha) * v.y + alpha * d.y
            v.z = (1 - alpha) * v.z + alpha * d.z

        # reseta inclinação visual ao reconstruir
        if alpha >= 1.0:
            self.frame_animacao = 0

    def DesenhaVertices(self):
        glPushMatrix()
        glTranslatef(self.position.x, self.position.y, self.position.z)
        glRotatef(self.rotation[3], self.rotation[0], self.rotation[1], self.rotation[2])

        # aplica rotação no vórtex
        if hasattr(self, 'frame_animacao') and self.frame_animacao > 0:
            inclinacao = min(360, self.frame_animacao * 2)
            glRotatef(inclinacao, 0, 0, 1)

        glColor3f(.0, .0, .0)
        glPointSize(8)

        for v in self.vertices:
            glPushMatrix()
            glTranslate(v.x, v.y, v.z)
            glutSolidSphere(.05, 20, 20)
            glPopMatrix()
        glPopMatrix()


    def DesenhaWireframe(self):
        glPushMatrix()
        glTranslatef(self.position.x, self.position.y, self.position.z)
        glRotatef(self.rotation[3], self.rotation[0], self.rotation[1], self.rotation[2])
        glColor3f(0, 0, 0)
        glLineWidth(2)

        for f in self.faces:
            glBegin(GL_LINE_LOOP)
            for iv in f:
                v = self.vertices[iv]
                glVertex(v.x, v.y, v.z)
            glEnd()

        glPopMatrix()

    def Desenha(self):
        glPushMatrix()
        glTranslatef(self.position.x, self.position.y, self.position.z)
        glRotatef(self.rotation[3], self.rotation[0], self.rotation[1], self.rotation[2])
        glColor3f(0.34, .34, .34)
        glLineWidth(2)

        for f in self.faces:
            glBegin(GL_TRIANGLE_FAN)
            for iv in f:
                v = self.vertices[iv]
                glVertex(v.x, v.y, v.z)
            glEnd()

        glPopMatrix()

    def ProximaPos(self):
        for i in range(len(self.vertices)):
            self.angle[i] += self.speed[i] * (1/30)
            x = self.radius[i] * math.cos(self.angle[i])
            z = self.radius[i] * math.sin(self.angle[i])
            self.vertices[i].x = x
            self.vertices[i].z = z

    def ResetEstado(self):
        for i in range(len(self.vertices)):
            self.vertices[i].x = self.vertices_original[i].x
            self.vertices[i].y = self.vertices_original[i].y
            self.vertices[i].z = self.vertices_original[i].z

        self.position = Ponto(0, 0, 0)
        self.rotation = (0, 0, 0, 0)
        self.frame_animacao = 0
        self.vortex_offset_angle = 0 

    def AtualizaConcentracao(self, alpha):
        for i in range(len(self.vertices)):
            v = self.vertices[i]
            v.x = (1 - alpha) * v.x
            v.y = (1 - alpha) * v.y
            v.z = (1 - alpha) * v.z

    def GerarEsferaVertices(self, raio=1.0):
            self.vertices_esfera_destino = []
            num_vertices = len(self.vertices_original)

            phi_increment = math.pi * (3 - math.sqrt(5)) 
            for i in range(num_vertices):
                y = 1 - (i / float(num_vertices - 1)) * 2 
                radius_at_y = math.sqrt(1 - y * y) 
                theta = phi_increment * i 

                x = math.cos(theta) * radius_at_y
                z = math.sin(theta) * radius_at_y

                ponto_esfera = Ponto(x * raio, y * raio, z * raio)
                self.vertices_esfera_destino.append(ponto_esfera)

    def AtualizaConcentracaoEsfera(self, alpha):
        if not self.vertices_esfera_destino:
           
            self.GerarEsferaVertices(raio=0.8) 

        for i in range(len(self.vertices)):
            v = self.vertices[i]
            d = self.vertices_esfera_destino[i % len(self.vertices_esfera_destino)]

            v.x = (1 - alpha) * v.x + alpha * d.x
            v.y = (1 - alpha) * v.y + alpha * d.y
            v.z = (1 - alpha) * v.z + alpha * d.z

    def AtualizaPulsacao(self, alpha):
        fator_expansao_max = 1.15 
        fator_contracao_min = 0.85 
        if alpha <= 0.5:
            progresso_subfase = alpha / 0.5 
            fator_escala = 1.0 + (fator_expansao_max - 1.0) * progresso_subfase
        else:
            progresso_subfase = (alpha - 0.5) / 0.5 
            fator_escala = fator_expansao_max - (fator_expansao_max - fator_contracao_min) * progresso_subfase
            amplitude = (fator_expansao_max - fator_contracao_min) / 2.0
            valor_medio = 1.0 
            fator_escala = valor_medio + amplitude * math.sin(alpha * 2 * math.pi)
       
        for i in range(len(self.vertices)):
            v = self.vertices[i]
            v.x = self.vertices_esfera_destino[i].x * fator_escala
            v.y = self.vertices_esfera_destino[i].y * fator_escala
            v.z = self.vertices_esfera_destino[i].z * fator_escala  

    def AtualizaConcentracaoNuvem(self, alpha, raio_nuvem=0.5):
        """
        Anima os vértices para que se concentrem em uma nuvem orgânica
        dentro de um raio específico ao redor da origem.
        """
        # Se ainda não geramos os destinos aleatórios para a nuvem, faça isso no primeiro frame
        if not hasattr(self, '_nuvem_destino_gerado') or not self._nuvem_destino_gerado:
            self._nuvem_destino_pontos = []
            for i in range(len(self.vertices)):
                # Gera um ponto aleatório dentro de uma esfera de raio 'raio_nuvem'
                # Usamos coordenadas esféricas para uma distribuição mais uniforme
                phi = random.uniform(0, 2 * math.pi)   # Latitude
                theta = random.uniform(0, math.pi)     # Longitude
                r = random.uniform(0, raio_nuvem)      # Distância do centro

                x_dest = r * math.sin(theta) * math.cos(phi)
                y_dest = r * math.sin(theta) * math.sin(phi)
                z_dest = r * math.cos(theta)

                self._nuvem_destino_pontos.append(Ponto(x_dest, y_dest, z_dest))
            self._nuvem_destino_gerado = True

        # Resetar a flag de nuvem destino quando o objeto for resetado globalmente
        # Isso é importante para que uma nova nuvem seja gerada em um novo ciclo da FSM.
        # Adicione self._nuvem_destino_gerado = False no seu Objeto3D.ResetEstado()

        for i in range(len(self.vertices)):
            v = self.vertices[i]
            d_nuvem = self._nuvem_destino_pontos[i] # Ponto de destino aleatório na nuvem

            # Interpolação linear para a posição aleatória dentro da nuvem
            v.x = (1 - alpha) * v.x + alpha * d_nuvem.x
            v.y = (1 - alpha) * v.y + alpha * d_nuvem.y
            v.z = (1 - alpha) * v.z + alpha * d_nuvem.z
    
    def ResetEstado(self):
        for i in range(len(self.vertices)):
            self.vertices[i].x = self.vertices_original[i].x
            self.vertices[i].y = self.vertices_original[i].y
            self.vertices[i].z = self.vertices_original[i].z

        self.position = Ponto(0, 0, 0)
        self.rotation = (0, 0, 0, 0)
        self.frame_animacao = 0
        self.vortex_offset_angle = 0 
        # NOVO: Resetar a flag de geração da nuvem
        self._nuvem_destino_gerado = False # Para que novos pontos aleatórios sejam gerados se o estado for re-entrado
        self._nuvem_destino_pontos = [] # Limpa os pontos também 

    def AtualizaVooCircularESaidaNuvem(self, alpha):
        # Assumimos que as partículas estão concentradas na origem (0,0,0) neste ponto.
        # A animação de Voo Circular e Saída será aplicada ao centro do objeto (self.position),
        # e as partículas que formam a nuvem (já concentradas na origem)
        # seguirão essa translação.

        raio_orbita = 4.0 # Raio da órbita circular para o centro da nuvem
        velocidade_angular = 2 * math.pi # Uma volta completa no estado

        # Calcula a posição X e Z para o CENTRO DA NUVEM (movendo o self.position do Objeto3D)
        self.position.x = raio_orbita * math.cos(alpha * velocidade_angular)
        self.position.z = raio_orbita * math.sin(alpha * velocidade_angular)

        # A altura da nuvem pode ser constante ou variar um pouco
        self.position.y = 0.5 + 0.5 * math.sin(alpha * 2 * math.pi) # Exemplo: Pequena variação de altura

        # Fase 2: Saída da Tela
        ponto_inicio_saida = 0.75 # Alpha a partir do qual a nuvem começa a sair
        if alpha >= ponto_inicio_saida:
            progresso_saida = (alpha - ponto_inicio_saida) / (1.0 - ponto_inicio_saida)

            fator_distancia = 1.0 + progresso_saida * 10.0 # Multiplica o raio por até 10x
            self.position.x = raio_orbita * fator_distancia * math.cos(alpha * velocidade_angular)
            self.position.z = raio_orbita * fator_distancia * math.sin(alpha * velocidade_angular)

            self.position.y += progresso_saida * 5.0 # Sobe 5 unidades

        # Opcional: Fazer a nuvem girar sobre seu próprio eixo enquanto voa
        self.rotation = (0, 1, 0, alpha * 720) # Gira em torno do próprio eixo Y