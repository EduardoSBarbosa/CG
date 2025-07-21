# 🌀 Animação Procedural 3D com Partículas em OpenGL
Este projeto apresenta uma animação procedural em 3D de uma cabeça, onde os próprios vértices do modelo 3D atuam como um sistema de partículas animado. A animação busca replicar comportamentos complexos observados no vídeo de referência `Particle Dreams` de Karl Sims, utilizando uma Máquina de Estados Finita (FSM) para orchestrar as transições entre diversas fases, incluindo estilhaçamento, formação de vórtex e reconstrução.

**Descrição:** O projeto simula a transformação de uma cabeça 3D em um sistema de partículas dinâmico. A animação se desenvolve através de 15 estados distintos (0 a 14) , que incluem movimentos iniciais da cabeça (inclinação, subida, queda) , fragmentação em partículas , reorganização em um vórtex , e sua subsequente reconstrução. Além de replicar a animação de referência, o projeto incorpora fases criativas adicionais, como a concentração em esferas , pulsação , e um voo circular com saída de cena.

## ✨ Funcionalidades

* **Animação Baseada em FSM:** Uma Máquina de Estados Finita com 15 estados (0 a 14) controla a sequência e a lógica dos movimentos das partículas e transformações do objeto.
* **Sistema de Partículas Dinâmico:** Os vértices de um modelo 3D (Human_Head.obj) são usados como partículas, que podem se estilhaçar, formar um vórtex, se concentrar em esferas e pulsar.
* **Replicação de Animação de Referência:** As fases iniciais da animação replicam movimentos específicos do vídeo "Particle Dreams" de Karl Sims (no intervalo de 0:26 a 0:43).
* **Fases Criativas Adicionais:** O projeto inclui 10 segundos extras de animação com dois movimentos distintos e criativos , como concentração em nuvem e voo circular com saída de cena.
* **Câmera Interativa:** O usuário pode controlar a câmera no ambiente 3D para visualizar a animação de diferentes ângulos (usando o mouse).
* **Controle de Reprodução:** A animação pode ser controlada via teclado, permitindo rodar, pausar, voltar ou avançar nos estados (PLAY, PAUSE, REWIND, FORWARD).
    * **Seta para Cima (↑):** Pausa/Retoma a animação (PLAY/PAUSE). 
    * **Seta para Esquerda (←):** Retorna ao estado anterior da FSM (REWIND). 
    * **Seta para Direita (→):** Avança para o próximo estado da FSM (FORWARD). 
    * **Seta para Baixo (↓):** Encerra o programa.

* **Captura de Frames:** Funcionalidade para capturar e salvar frames da animação em tempo real como imagens PNG. Pressione a tecla 'c' para iniciar ou pausar a captura de frames. Os frames são salvos na pasta `captured_frames`. 
* **Áudio de Fundo:** Integração de uma música de fundo que pode ser pausada e retomada durante a execução. Pressione a tecla 'm' para pausar ou retomar a música de fundo.
* **Visualização 3D com OpenGL:** Renderização gráfica da cena e dos objetos em um ambiente 3D, utilizando projeção perspectiva , iluminação , e culling de faces para otimização.

## 🚀 Como Executar
Para rodar este projeto, siga os passos abaixo:

### Pré-requisitos

Certifique-se de ter o Python instalado (versão 3.11.9 recomendada).
Você precisará das seguintes bibliotecas Python:
* `pygame` 
* `PyOpenGL`
* `Pillow` (PIL) 

Você pode instalá-las usando pip:

```bash
pip install pygame PyOpenGL Pillow
```

### Estrutura do Projeto
Certifique-se de que os seguintes arquivos estejam no mesmo diretório:

* **main.py** (Script principal da aplicação) 
* **Objeto3D.py** (Define a classe para carregar e manipular modelos 3D) 
* **Ponto.py** (Define a classe para pontos 3D e operações geométricas)
* **Linha.py** (Define a classe para representar segmentos de reta) 
* **Human_Head.obj** (Modelo 3D da cabeça, base para as partículas) 
* **Numb.mp3** (Arquivo de música de fundo) 

### Execução
Após instalar as dependências e organizar os arquivos, execute o projeto a partir do terminal ou prompt de comando:

```bash
python main.py
```

