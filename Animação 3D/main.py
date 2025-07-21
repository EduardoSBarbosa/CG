# --- Versão atualizada com FSM integrada ---
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

import time
import sys
import os
import math
from PIL import Image

from Objeto3D import *

import pygame.mixer # Adicione esta linha

o: Objeto3D

# --- Controle de tempo ---
tempo_antes = time.time()
soma_dt = 0
animacao_ativa = True

# --- Câmera interativa ---
cam_angulo_x = 45
cam_angulo_y = 30
cam_dist = 10
mouse_x = 0
mouse_y = 0
arrastando = False

# --- FSM da animação ---
estado_animacao = 0
frame_animacao = 0
TRANSICOES = {
    0: 30,   # Cabeça parada
    1: 30,   # Inclinação
    2: 30,   # Subida
    3: 60,   # Queda
    4: 30,   # Estilhaço
    5: 60,   # partículas descendo até o chão
    6: 90,   # Vórtex
    7: 30,   # Reconstrução
    8: 60,   # NOVO ESTADO: Rotação Completa e Aceleração
    9: 60,   # NOVO ESTADO: Concentração em Esfera
    10: 60,  # NOVO ESTADO: Pulsação/Expansão e Contração
    11: 30,  # NOVO ESTADO: Concentração no centro
    12: 60,  # NOVO ESTADO: Explosão final
    13: 60,  # NOVO ESTADO: Reconcentração em Nuvem (pós-explosão)
    14: 120, # NOVO ESTADO: Voo Circular da Nuvem e Saída da Tela
}

# --- Captura de frames ---
capturando_frames = False
frame_count_capture = 0
frame_output_folder = "captured_frames"
os.makedirs(frame_output_folder, exist_ok=True)

# --- Inicialização ---
def captura_frame():
    global frame_count_capture

    viewport = glGetIntegerv(GL_VIEWPORT)
    x, y, width, height = viewport[0], viewport[1], viewport[2], viewport[3]

    pixel_data = glReadPixels(x, y, width, height, GL_RGB, GL_UNSIGNED_BYTE)

    image = Image.frombytes("RGB", (width, height), pixel_data)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)

    filename = os.path.join(frame_output_folder, f"frame_{frame_count_capture:05d}.png")
    try:
        image.save(filename)
        frame_count_capture += 1
    except Exception as e:
        print(f"ERRO: Erro ao salvar frame {filename}: {e}. Verifique as permissões da pasta.")

# --- Inicialização da Música ---
def inicia_musica():
    try:
        # Substitua 'musica_fundo.mp3' pelo nome do seu arquivo de música
        # AGORA É 'Numb.mp3'
        pygame.mixer.music.load('Numb.mp3') 
        pygame.mixer.music.play(-1) # -1 faz a música tocar em loop infinito
        pygame.mixer.music.set_volume(0.5) # Ajusta o volume (0.0 a 1.0)
        print("Música de fundo iniciada.")
    except Exception as e:
        print(f"ERRO: Não foi possível carregar ou tocar a música (em inicia_musica): {e}")
        print("Verifique se o arquivo de música existe e o formato está correto (ex: .mp3, .wav).")

def init():
    global o
    glClearColor(0.5, 0.5, 0.9, 1.0)
    glClearDepth(1.0)

    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    o = Objeto3D()
    o.LoadFile('Human_Head.obj')

    DefineLuz()
    PosicUser() 

    # Isso garante que a música seja carregada e tocada *após* a inicialização gráfica inicial.
    inicia_musica()

def DefineLuz():
    luz_ambiente = [0.4, 0.4, 0.4]
    luz_difusa = [0.7, 0.7, 0.7]
    luz_especular = [0.9, 0.9, 0.9]
    posicao_luz = [2.0, 3.0, 0.0]
    especularidade = [1.0, 1.0, 1.0]

    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_LIGHTING)
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, luz_ambiente)
    glLightfv(GL_LIGHT0, GL_AMBIENT, luz_ambiente)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, luz_difusa)
    glLightfv(GL_LIGHT0, GL_SPECULAR, luz_especular)
    glLightfv(GL_LIGHT0, GL_POSITION, posicao_luz)
    glEnable(GL_LIGHT0)

    glEnable(GL_COLOR_MATERIAL)
    glMaterialfv(GL_FRONT, GL_SPECULAR, especularidade)
    glMateriali(GL_FRONT, GL_SHININESS, 51)

def PosicUser():
    global cam_angulo_x, cam_angulo_y, cam_dist

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, 16/9, 0.01, 50)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    eye_x = cam_dist * math.cos(math.radians(cam_angulo_y)) * math.sin(math.radians(cam_angulo_x))
    eye_y = cam_dist * math.sin(math.radians(cam_angulo_y))
    eye_z = cam_dist * math.cos(math.radians(cam_angulo_y)) * math.cos(math.radians(cam_angulo_x))

    gluLookAt(eye_x, eye_y, eye_z, 0, 0, 0, 0, 1, 0)

def DesenhaLadrilho():
    glColor3f(0.5, 0.5, 0.5)
    glBegin(GL_QUADS)
    glNormal3f(0, 1, 0)
    glVertex3f(-0.5, 0.0, -0.5)
    glVertex3f(-0.5, 0.0, 0.5)
    glVertex3f(0.5, 0.0, 0.5)
    glVertex3f(0.5, 0.0, -0.5)
    glEnd()

    glColor3f(1, 1, 1)
    glBegin(GL_LINE_STRIP)
    glNormal3f(0, 1, 0)
    glVertex3f(-0.5, 0.0, -0.5)
    glVertex3f(-0.5, 0.0, 0.5)
    glVertex3f(0.5, 0.0, 0.5)
    glVertex3f(0.5, 0.0, -0.5)
    glEnd()

def DesenhaPiso():
    glPushMatrix()
    glTranslated(-20, -1, -10)
    for x in range(-20, 20):
        glPushMatrix()
        for z in range(-20, 20):
            DesenhaLadrilho()
            glTranslated(0, 0, 1)
        glPopMatrix()
        glTranslated(1, 0, 0)
    glPopMatrix()

def DesenhaCubo():
    glPushMatrix()
    glColor3f(1, 0, 0)
    glTranslated(0, 0.5, 0)
    glutSolidCube(1)

    glColor3f(0.5, 0.5, 0)
    glTranslated(0, 0.5, 0)
    glRotatef(90, -1, 0, 0)
    glRotatef(45, 0, 0, 1)
    glutSolidCone(1, 1, 4, 4)
    glPopMatrix()

# --- FSM ---
def AtualizaAnimacao():
    global estado_animacao, frame_animacao, o
    frame_animacao += 1

    if estado_animacao in TRANSICOES and frame_animacao > TRANSICOES[estado_animacao]:
        if estado_animacao < max(TRANSICOES.keys()):
            estado_animacao += 1
            frame_animacao = 0
        else:
            frame_animacao = TRANSICOES[estado_animacao]

    if estado_animacao == 0:
        pass
    elif estado_animacao == 1:
        o.rotation = (1, 0, 0, -15 * (frame_animacao / TRANSICOES[1]))
    elif estado_animacao == 2:
        o.position.y = (2.5 * frame_animacao / TRANSICOES[2])
    elif estado_animacao == 3:
        if frame_animacao == 0:
            o.position.y = 2.5  # Garante que sempre caia da altura correta
        else:
            o.position.y = 2.5 * (1 - (frame_animacao / TRANSICOES[3]))
    elif estado_animacao == 4:
        o.AtualizaEstilhaçamento()
    elif estado_animacao == 5:
        o.DepositaParticulasNoChao()
    elif estado_animacao == 6:
        o.AtualizaVortex(frame_animacao)
    elif estado_animacao == 7:
        alpha = frame_animacao / TRANSICOES[7]
        o.Reconstrucao(alpha)
    elif estado_animacao == 8:
        duracao_estado = TRANSICOES[8]
        progresso = frame_animacao / duracao_estado
        angulo_rotacao_atual = 720 * progresso # Rota duas vezes (720 graus) com aceleração suave
        o.rotation = (0, 1, 0, angulo_rotacao_atual) 
    elif estado_animacao == 9:
        duracao_estado = TRANSICOES[9]
        alpha = frame_animacao / duracao_estado
        o.AtualizaConcentracaoEsfera(alpha)
    elif estado_animacao == 10:
        duracao_estado = TRANSICOES[10]
        alpha = frame_animacao / duracao_estado
        o.AtualizaPulsacao(alpha) 
    elif estado_animacao == 11: 
        alpha = frame_animacao / TRANSICOES[11]
        o.AtualizaConcentracao(alpha) 
    elif estado_animacao == 12: # Explosão final
        if frame_animacao == 1: 
            for i in range(len(o.vertices)):
                o.vx[i] = random.uniform(-0.2, 0.2)
                o.vy[i] = random.uniform(0.1, 0.4)
                o.vz[i] = random.uniform(-0.2, 0.2)

        for i in range(len(o.vertices)):
            o.vertices[i].x += o.vx[i]
            o.vertices[i].y += o.vy[i]
            o.vertices[i].z += o.vz[i]
            o.vy[i] -= 0.01 
    elif estado_animacao == 13: # REVISADO: Reconcentração em Nuvem (orgânica)
        duracao_estado = TRANSICOES[13]
        alpha = frame_animacao / duracao_estado
        # Chama a nova função para concentrar em uma nuvem orgânica
        o.AtualizaConcentracaoNuvem(alpha, raio_nuvem= 5) # Ajuste o raio_nuvem aqui!
        # Um raio_nuvem de 0.5 a 1.0 deve criar uma boa nuvem para a cabeça.

    elif estado_animacao == 14: # Voo Circular da Nuvem e Saída da Tela (lógica permanece a mesma)
        duracao_estado = TRANSICOES[14]
        alpha = frame_animacao / duracao_estado
        o.AtualizaVooCircularESaidaNuvem(alpha)
        
    if capturando_frames:
        captura_frame()

# --- Idle ---
def Animacao():
    global soma_dt, tempo_antes
    if not animacao_ativa:
        return

    tempo_agora = time.time()
    delta_time = tempo_agora - tempo_antes
    tempo_antes = tempo_agora
    soma_dt += delta_time

    if soma_dt > 1.0 / 30:
        soma_dt = 0
        AtualizaAnimacao()
        glutPostRedisplay()

def desenha():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)

    DesenhaPiso()
    o.DesenhaVertices()

    glutSwapBuffers()

def teclado(key, x, y):
    global estado_animacao, frame_animacao, capturando_frames, frame_count_capture
    print(f"Tecla pressionada: {key}") 
    if key == b'c':
        capturando_frames = not capturando_frames
        if capturando_frames:
            frame_count_capture = 0
            print("Iniciando captura de frames. Pressione 'c' novamente para pausar.")
        else:
            print("Captura de frames PAUSADA.") 
    elif key == b'm': # Adicione esta linha para controlar a música
        # AQUI: Adicione a verificação se o mixer está inicializado
        if pygame.mixer.get_init(): # Verifica se o mixer foi inicializado com sucesso
            if pygame.mixer.music.get_busy(): # Se a música está tocando
                pygame.mixer.music.pause()
                print("Música PAUSADA.")
            else: # Se a música está pausada ou parada
                pygame.mixer.music.unpause()
                print("Música RETOMADA.")
        else:
            print("ERRO: Mixer Pygame não está inicializado para controle de música.")
    elif key == b'q':
        if pygame.mixer.get_init(): # Verifica antes de tentar parar a música
            if pygame.mixer.music.get_busy(): 
                pygame.mixer.music.stop()
        glutLeaveMainLoop()
        print("Saindo do programa.")
    glutPostRedisplay()

def teclas_especiais(tecla, x, y):
    global animacao_ativa, estado_animacao, frame_animacao

    if tecla == GLUT_KEY_UP:
        animacao_ativa = not animacao_ativa
    elif tecla == GLUT_KEY_LEFT:
        estado_animacao = max(0, estado_animacao - 1)
        frame_animacao = 0
        o.ResetEstado()
    elif tecla == GLUT_KEY_RIGHT:
        estado_animacao = min(max(TRANSICOES.keys()), estado_animacao + 1)
        frame_animacao = 0
        o.ResetEstado()
    elif tecla == GLUT_KEY_DOWN:
        os._exit(0)

    glutPostRedisplay()

def mouse(botao, estado, x, y):
    global mouse_x, mouse_y, arrastando
    if estado == GLUT_DOWN:
        arrastando = True
        mouse_x, mouse_y = x, y
    else:
        arrastando = False

def movimento_mouse(x, y):
    global mouse_x, mouse_y, cam_angulo_x, cam_angulo_y
    if arrastando:
        dx = x - mouse_x
        dy = y - mouse_y
        cam_angulo_x += dx * 0.5
        cam_angulo_y += dy * 0.5
        cam_angulo_y = max(-89, min(89, cam_angulo_y))
        mouse_x, mouse_y = x, y
        PosicUser()
        glutPostRedisplay()

def main():

    # AQUI: Inicialize o mixer do pygame ANTES do GLUT
    try:
        pygame.mixer.init()
        print("Pygame Mixer inicializado com sucesso em main()!")
        # Não carregar a música aqui, pois ela será carregada em init() via inicia_musica()
    except Exception as e:
        print(f"ERRO: Não foi possível inicializar o mixer Pygame (em main()): {e}")
        print("Isso pode ocorrer se não houver um dispositivo de áudio disponível.")
        # sys.exit(1)

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b'Computacao Grafica - 3D')

    init()

    glutDisplayFunc(desenha)
    glutKeyboardFunc(teclado)
    glutSpecialFunc(teclas_especiais)
    glutMouseFunc(mouse)
    glutMotionFunc(movimento_mouse)
    glutIdleFunc(Animacao)

    try:
        glutMainLoop()
    except SystemExit:
        pass

if __name__ == '__main__':
    main()