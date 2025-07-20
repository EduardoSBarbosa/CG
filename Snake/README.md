# 🐍 Jogo da Cobrinha com OpenGL

Um clássico jogo da cobrinha desenvolvido em Python, utilizando a biblioteca Pygame e renderização com OpenGL. [cite_start]Este projeto oferece uma experiência de jogo tradicional com um toque visual diferenciado e alvos com movimento dinâmico. [cite: 7, 8, 9, 13]

[cite_start]**Descrição:** A simulação apresenta uma cobrinha controlada pelo jogador via teclado. [cite: 18] [cite_start]Alvos se movem em trajetórias predefinidas lidas do arquivo `Paths_D.txt` (Arquivo de texto com coordenadas (x,y,frame)). [cite: 8, 14, 28] [cite_start]Ao colidir com um alvo, a cobrinha o absorve, cresce e sua pontuação é incrementada. [cite: 20, 21] [cite_start]O jogo termina ao final dos frames e exibe o score final no console. [cite: 22]

## ✨ Funcionalidades

* [cite_start]**Movimentação Clássica:** Controle a cobrinha com as setas do teclado. 
* [cite_start]**Comer Alvos:** A cobrinha cresce ao colidir com os alvos. [cite: 20, 312]
* [cite_start]**Alvos com Trajetória:** Os alvos se movem seguindo caminhos predefinidos do arquivo `Paths_D.txt`, adicionando um desafio dinâmico. [cite: 8, 14, 19, 313]
* **Travessia de Tela:** Quando a cobrinha sai por uma borda da janela, ela reaparece na borda oposta (característica clássica do jogo).
* **Cor de Fundo Personalizada:** A tela de fundo possui um tom de verde claro para uma experiência visual agradável.

## 🚀 Como Executar

Para rodar este jogo, siga os passos abaixo:

### Pré-requisitos

[cite_start]Certifique-se de ter o Python instalado (versão 3.11.9 recomendada)[cite: 26, 41].
Você precisará das seguintes bibliotecas Python:
* [cite_start]`pygame` [cite: 25, 41]
* [cite_start]`PyOpenGL` [cite: 24, 41]

Você pode instalá-las usando pip:

```bash
pip install pygame PyOpenGL