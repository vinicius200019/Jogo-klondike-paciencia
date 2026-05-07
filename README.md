# 🃏 Klondike Python | Jogo de Paciência Clássico

<p align="center">
  <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" />
  <img src= https://upload.wikimedia.org/wikipedia/commons/b/be/Pygame_logo.svg utm_source=commons.wikimedia.org&utm_campaign=index&utm_content=original/>
</p>

---

## 📝 Sobre o Projeto

O Klondike Python é uma recriação digital do clássico jogo de cartas Paciência (Klondike). Desenvolvido inteiramente em Python utilizando a biblioteca Pygame, o projeto combina a lógica complexa das regras do jogo com uma interface gráfica interativa, oferecendo recursos modernos como dicas visuais e histórico de jogadas.

> **Status do Projeto:** ✔️ Concluído / Funcional

---

## ✨ Funcionalidades Principais

* **🎮 Interface Gráfica (GUI)** Sistema de login com autenticação via PHP e MySQL.
* **↩️ Sistema de Desfazer:** Errou a jogada? O jogo armazena até 50 estados anteriores para você desfazer movimentos (via botão ou Ctrl+Z).
* **💡 Sistema de Dicas Inteligente:** Destaca visualmente no tabuleiro quais cartas podem ser movidas e para onde.
* **📊 Métricas de Partida:** Acompanhamento em tempo real do tempo de jogo e contador de movimentos.
* **📜 Estratégias e Regras:** Menu in-game contendo dicas e estratégias para vencer a partida.
* **🏆 Tela de Vitória:** Animação e tela de parabenização ao completar as fundações, exibindo seu tempo e total de movimentos.

---

## ⚙️ Tecnologias Utilizadas

Este projeto utiliza um ambiente Python focado em desenvolvimento de jogos 2D:
1.  **Linguagem Base:** Python 3.x para toda a lógica orientada a objetos (classes Carta, JogoKlondike e InterfaceJogo).
2.  **Renderização Gráfica:** Pygame para manipulação de janelas, eventos de mouse/teclado, desenho de formas (cartas, botões) e controle de FPS.
3.  **Bibliotecas Padrão:** random (embaralhamento), time (controle de dicas) e sys (sistema).

---

## 🚀 Como Configurar o Ambiente

Para rodar o Klondike localmente, siga estes passos:

### 1. Pré-requisitos
Certifique-se de ter o **Python**(versão 3.6 ou superior) instalado na sua máquina.

### 2. Instalação do Pygame
Abra o seu terminal e instale a biblioteca gráfica necessária:
```bash
pip install pygame
```

### 3. Download do Projeto
Clone este repositório para a sua máquina local:
```bash
git clone https://github.com/SEU_USUARIO/klondike_python.git
```

---

## 📈 Fluxo do Sistema

[SISTEMA] Gera o baralho (52 cartas), embaralha e distribui nas 7 colunas do Tableau e no Estoque

↓

[JOGADOR] Clica em uma carta (Estoque, Descarte ou Tableau)

↓

[SISTEMA] Valida a cor, o naipe e o valor sequencial da carta selecionada em relação ao destino

↓

[SISTEMA] Se válido, move a carta, atualiza o histórico (para a função Desfazer) e conta o movimento

↓

[JOGADOR] Preenche todas as 4 fundações do Ás ao Rei

↓

[SISTEMA] Detecta a condição de vitória e exibe a tela de Parabéns com os status da partida

---

## 📂 Estrutura do Projeto

Abaixo está a organização dos arquivos e pastas do repositório:

```text
klondike_python/
│
├── 📄 main.py               # Arquivo principal que gerencia a interface Pygame e eventos
└── 📄 klondike_game.py      # Módulo contendo a lógica e regras do jogo (State Manager)
```

---

## 🚀 Como Rodar na Sua Máquina

Com as bibliotecas instaladas e o repositório clonado, navegue até a pasta raiz do projeto pelo terminal e execute o arquivo principal:

```bash
cd klondike_python
python main.py
```

A janela do jogo será aberta automaticamente!

## ⌨️ Desenvolvedores

<strong>Vinícius</strong>
























