# 🦠 Jogo Agar.io 2D com OpenGL

Uma simulação interativa baseada no clássico jogo Agar.io, desenvolvida em Python com Pygame para gerenciamento da janela e eventos, e OpenGL para renderização gráfica 2D. Este projeto explora conceitos de visualização 2D, controle de entidade e lógica de absorção com pontuação.

**Descrição:** A simulação apresenta um círculo controlado pelo jogador via teclado. Alvos se movem em trajetórias predefinidas lidas do arquivo `Paths_D.txt` (Arquivo de texto com coordenadas (x,y,frame)). A simulação envolve interações como colisões e crescimento da entidade controlável, além de integrar conceitos de visualização 2D, controle por teclado e lógica de absorção com pontuação.

## ✨ Funcionalidades

* **Movimentação por Teclado:** Controle o personagem principal utilizando as setas do teclado.
* **Alvos com Trajetória:** Múltiplos círculos se movem seguindo caminhos predefinidos extraídos do arquivo `Paths_D.txt`, adicionando um elemento dinâmico ao jogo.
* **Mecânica de Absorção:** Ao colidir com um alvo, o personagem o absorve, aumentando seu raio e pontuação.
* **Visualização 2D com OpenGL:** Renderização de formas geométricas (círculos) e cores distintas para o jogador e os alvos.
* **Pontuação e Encerramento:** O jogo acompanha a pontuação do jogador e finaliza automaticamente quando todos os frames de animação dos alvos terminam, exibindo o score final no console.

## 🚀 Como Executar

Para rodar este jogo, siga os passos abaixo:

### Pré-requisitos

Certifique-se de ter o Python instalado (versão 3.11.9 recomendada).
Você precisará das seguintes bibliotecas Python:
* `pygame`
* `PyOpenGL`

Você pode instalá-las usando pip:

```bash
pip install pygame PyOpenGL 
```

Você pode rodá-lo usando o comando:

```bash
python main.py
```