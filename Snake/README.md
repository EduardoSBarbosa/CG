# 🐍 Jogo da Cobrinha com OpenGL

Um clássico jogo da cobrinha desenvolvido em Python, utilizando a biblioteca Pygame e renderização com OpenGL. Este projeto oferece uma experiência de jogo tradicional com um toque visual diferenciado e alvos com movimento dinâmico.

**Descrição:** A simulação apresenta uma cobrinha controlada pelo jogador via teclado. Alvos se movem em trajetórias predefinidas lidas do arquivo `Paths_D.txt` (Arquivo de texto com coordenadas (x,y,frame)). Ao colidir com um alvo, a cobrinha o absorve, cresce e sua pontuação é incrementada. O jogo termina ao final dos frames e exibe o score final no console.

## ✨ Funcionalidades

* **Movimentação Clássica:** Controle a cobrinha com as setas do teclado. 
* **Comer Alvos:** A cobrinha cresce ao colidir com os alvos.
* **Alvos com Trajetória:** Os alvos se movem seguindo caminhos predefinidos do arquivo `Paths_D.txt`, adicionando um desafio dinâmico.
* **Travessia de Tela:** Quando a cobrinha sai por uma borda da janela, ela reaparece na borda oposta (característica clássica do jogo).

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
