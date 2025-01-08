# Atividade-livre---OO

# Jogo de Tiro ao Alvo

Este é um jogo simples de tiro ao alvo desenvolvido utilizando a biblioteca Pygame. O jogador utiliza uma mira para acertar os alvos que aparecem na tela, acumulando pontos conforme os alvos são atingidos. O jogo inclui uma mecânica de tempo limitado, pausas e registro de recordes.

## Requisitos do Sistema

- Python 3.x
- Pygame

## Estrutura do Projeto

- `jogo.py`: Script principal do jogo.
- `Constants.py`: Contém as constantes utilizadas no jogo, como dimensões da tela e caminhos para os recursos.
- `assets/`: Pasta contendo imagens e sons usados no jogo.

## Classes Principais

- **GameState**: Gerencia o estado geral do jogo, incluindo a pontuação, tempo e controle de pausas.
- **Alvo**: Representa os alvos que o jogador deve acertar. Herda de `pygame.sprite.Sprite`.
- **Mira**: Representa a mira controlada pelo jogador. Também herda de `pygame.sprite.Sprite` e interage com os alvos para detecção de colisões.

## Funcionalidades

- **Salvar Jogo**: O jogador pode salvar o progresso durante o jogo ou na tela final, permitindo continuar depois.
- **Carregar Jogo**: O jogo salvo pode ser carregado para continuar de onde parou, incluindo o recorde anterior.
- **Recorde**: O recorde de pontuação é salvo e carregado junto com o estado do jogo.

## Configuração

1. Clone este repositório:

    ```bash
    git clone https://github.com/CamilaSilvaC/Atividade-livre---OO
    ```

2. Instale as dependências necessárias:

    ```bash
    pip install pygame
    ```
3. Navegue até o diretório do projeto:

    ```bash
    cd tiro-ao-alvo/jogo
    ```

## Como Jogar

1. Execute o script principal:

    ```bash
    python jogo.py
    ```

2. Utilize o mouse para mover a mira.
3. Clique com o mouse para atirar nos alvos.
4. O jogo termina quando o tempo se esgota. Você pode pausar o jogo pressionando a tecla **ESC**.
5. Pressione **S** para salvar o jogo a qualquer momento, inclusive na tela final.



