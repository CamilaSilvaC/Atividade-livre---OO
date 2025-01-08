# Atividade-livre---OO

Descrição
Este é um jogo simples de tiro ao alvo desenvolvido utilizando a biblioteca Pygame. O jogador utiliza uma mira para acertar os alvos que aparecem na tela, acumulando pontos conforme os alvos são atingidos. O jogo inclui uma mecânica de tempo limitado, pausas e registro de recordes.
Requisitos do Sistema
Python 3.x
Pygame
Configuração
Clone este repositório:
 git clone <url-do-repositorio>


Instale as dependências necessárias:
 pip install pygame


Como Jogar
Execute o script principal:
 python jogo.py


Utilize o mouse para mover a mira.
Clique com o botão esquerdo do mouse para atirar nos alvos.
O jogo termina quando o tempo se esgota. Você pode pausar o jogo pressionando a tecla ESC.
Estrutura do Projeto
jogo.py: Script principal do jogo.
Constants.py: Contém as constantes utilizadas no jogo, como dimensões da tela e caminhos para os recursos.
assets/: Pasta contendo imagens e sons usados no jogo.
Classes Principais
GameState
Gerencia o estado geral do jogo, incluindo a pontuação, tempo e controle de pausas.
Alvo
Representa os alvos que o jogador deve acertar. Herda de pygame.sprite.Sprite.
Mira
Representa a mira controlada pelo jogador. Também herda de pygame.sprite.Sprite e interage com os alvos para detecção de colisões.
