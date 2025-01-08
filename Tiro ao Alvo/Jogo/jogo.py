import pygame
import random
import sys
import Constants

class GameState:
    def __init__(self):
        # Inicializa os atributos do estado do jogo
        self.pontos = 0  # Pontuação atual
        self.timer = 1800  # Temporizador em frames (30 segundos)
        self.recorde = 0  # Recorde de pontuação
        self.game_paused = False  # Indica se o jogo está pausado
        self.finalizar = False  # Indica se o jogo deve terminar
        self.tempo_acabou = False  # Indica se o tempo do jogo acabou

    def reset(self):
        # Reseta a pontuação e o timer
        self.pontos = 0
        self.timer = 1800  # Reinicia o tempo
        self.tempo_acabou = False

    def update(self):
        # Atualiza o estado do jogo quando o timer atinge zero
        if self.timer < 0:
            self.timer = 0  # Garante que o timer não fique negativo
            if self.pontos > self.recorde:
                self.recorde = self.pontos  # Atualiza o recorde
            self.tempo_acabou = True  # Indica que o tempo acabou


class Alvo(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        # Inicializa o sprite do alvo
        super().__init__()
        self.image = pygame.image.load(Constants.ALVO).convert_alpha()  # Carrega a imagem do alvo
        self.image = pygame.transform.scale(self.image, (100, 100))  # Redimensiona a imagem
        self.rect = self.image.get_rect()  # Obtém o retângulo da imagem
        self.rect.center = [pos_x, pos_y]  # Define a posição inicial


class Mira(pygame.sprite.Sprite):
    def __init__(self):
        # Inicializa o sprite da mira
        super().__init__()
        self.image = pygame.image.load(Constants.MIRA).convert_alpha()  # Carrega a imagem da mira
        self.image = pygame.transform.scale(self.image, (50, 50))  # Redimensiona a imagem
        self.rect = self.image.get_rect()  # Obtém o retângulo da imagem
        self.sound = pygame.mixer.Sound(Constants.DISPARO)  # Carrega o som do disparo

    def update(self):
        # Atualiza a posição da mira para seguir o cursor do mouse
        self.rect.center = pygame.mouse.get_pos()

    def shoot(self, grupo_de_alvos):
        # Realiza o disparo e verifica colisões com os alvos
        global game_state
        self.sound.play()  # Toca o som do disparo

        # Verifica colisões entre a mira e os alvos
        colisions = pygame.sprite.spritecollide(self, grupo_de_alvos, False)
        for colision in colisions:
            game_state.pontos += 1  # Incrementa a pontuação
            colision.kill()  # Remove o alvo atingido
            # Cria um novo alvo em uma posição aleatória
            alvo = Alvo(random.randrange(0, Constants.LARGURA), random.randrange(0, Constants.ALTURA))
            grupo_de_alvos.add(alvo)

def menu_inicial(screen, font):
    """ Exibe a tela de menu inicial."""
    running = True
    while running:
        # Preenche a tela com a cor de fundo
        screen.fill((49, 102, 63))

        # Renderiza o texto de boas-vindas
        titulo = font.render("Bem-vindo ao jogo Tiro ao Alvo", True, (255, 255, 255))
        titulo_rect = titulo.get_rect(center=(Constants.LARGURA / 2, Constants.ALTURA / 2 - 70))
        screen.blit(titulo, titulo_rect)

        # Renderiza a instrução para iniciar
        instrucao_font = pygame.font.Font(Constants.FONTE, 18)  # Fonte menor para as instruções
        instrucao = instrucao_font.render("Clique em ENTER para iniciar", True, (255, 255, 255))
        instrucao_rect = instrucao.get_rect(center=(Constants.LARGURA / 2, Constants.ALTURA / 2 - 30))
        screen.blit(instrucao, instrucao_rect)

        # Renderiza o aviso sobre pausa
        pausa = instrucao_font.render("Pressione ESC para pausar o jogo", True, (255, 255, 255))
        pausa_rect = pausa.get_rect(center=(Constants.LARGURA / 2, Constants.ALTURA / 2 + 10))
        screen.blit(pausa, pausa_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # Sai do jogo
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Tecla ENTER
                    running = False  # Sai do menu

        pygame.display.flip()  # Atualiza a tela


def tela_fim_jogo(screen, font, recorde):
    """ Exibe a tela de fim de jogo quando o tempo acaba."""
    running = True
    while running:
        # Preenche a tela com a cor de fundo
        screen.fill((49, 102, 63))

        # Renderiza o texto de fim de jogo e o recorde
        fim_texto = font.render("Tempo Esgotado!", True, (255, 255, 255))
        fim_texto_rect = fim_texto.get_rect(center=(Constants.LARGURA / 2, Constants.ALTURA / 2 - 50))
        screen.blit(fim_texto, fim_texto_rect)

        recorde_texto = font.render(f"Recorde: {recorde}", True, (255, 255, 255))
        recorde_texto_rect = recorde_texto.get_rect(center=(Constants.LARGURA / 2, Constants.ALTURA / 2))
        screen.blit(recorde_texto, recorde_texto_rect)

        # Renderiza a instrução para reiniciar
        instrucao_font = pygame.font.Font(Constants.FONTE, 18)  # Fonte menor para as instruções
        instrucao = instrucao_font.render("Pressione ENTER para jogar novamente", True, (255, 255, 255))
        instrucao_rect = instrucao.get_rect(center=(Constants.LARGURA / 2, Constants.ALTURA / 2 + 50))
        screen.blit(instrucao, instrucao_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # Sai do jogo
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Tecla ENTER para reiniciar
                    running = False  # Sai da tela de fim de jogo

        pygame.display.flip()  # Atualiza a tela


pygame.init()

# Definindo o estado do jogo
game_state = GameState()

# Configura a tela principal
screen = pygame.display.set_mode((Constants.LARGURA, Constants.ALTURA))

# Carrega o background do jogo
bg = pygame.image.load(Constants.BG).convert()
bg = pygame.transform.scale(bg, (Constants.LARGURA, Constants.ALTURA))

clock = pygame.time.Clock()

# Carrega a fonte para textos
font = pygame.font.Font(Constants.FONTE, 25)
pygame.display.set_caption('Tiro ao alvo')

# Cria um grupo para os alvos
grupo_de_alvos = pygame.sprite.Group()

# Inicializa 20 alvos em posições aleatórias
for i in range(20):
    alvo = Alvo(random.randrange(0, Constants.LARGURA), random.randrange(0, Constants.ALTURA))
    grupo_de_alvos.add(alvo)

# Inicializa a mira
mira = Mira()
mira_group = pygame.sprite.Group()
mira_group.add(mira)

# Exibindo o menu inicial
menu_inicial(screen, font)

while not game_state.finalizar:
    if game_state.tempo_acabou:
        # Exibe a tela de fim de jogo
        tela_fim_jogo(screen, font, game_state.recorde)
        game_state.reset()  # Reinicia o estado do jogo

    elif not game_state.game_paused:
        pygame.mouse.set_visible(False)  # Esconde o cursor do mouse

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # Sai do jogo
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # ESC para pausar
                    game_state.game_paused = not game_state.game_paused

            if event.type == pygame.MOUSEBUTTONDOWN:
                mira.shoot(grupo_de_alvos)  # Realiza o disparo

        # Atualiza o background
        screen.blit(bg, (0, 0))
        # Desenha os alvos e a mira na tela
        grupo_de_alvos.draw(screen)
        mira_group.draw(screen)
        mira_group.update()

        # Exibe a pontuação
        score = font.render(f'Pontos: {game_state.pontos}', True, (0, 0, 0))
        screen.blit(score, (50, 50))

        # Exibe o tempo restante
        tempo = font.render(f'Tempo: {game_state.timer / 60:.1f} s', True, (0, 0, 0))
        screen.blit(tempo, (50, 100))

        # Reduz o timer a cada frame
        game_state.timer -= 1

        # Atualiza o estado do jogo
        game_state.update()

    else:
        # Tela de pausa
        screen.fill((104, 176, 123))  # Cor de fundo da pausa
        pygame.mouse.set_visible(True)  # Mostra o cursor do mouse
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # ESC para voltar ao jogo
                    game_state.game_paused = not game_state.game_paused

            if event.type == pygame.QUIT:
                pygame.quit()  # Sai do jogo
                sys.exit()

        # Exibe mensagens de pausa e recorde
        pause = font.render(f"PRECIONE ESC PARA INICIAR", True, (255, 255, 255))
        points = font.render(f"RECORDE: {game_state.recorde}", True, (255, 255, 255))

        pause_rect = pause.get_rect(center=(Constants.LARGURA / 2, Constants.ALTURA / 2))
        points_rect = points.get_rect(center=(Constants.LARGURA / 2, Constants.ALTURA / 2 - 50))

        screen.blit(pause, pause_rect)
        screen.blit(points, points_rect)

    pygame.display.flip()  # Atualiza a tela
    clock.tick(60)  # Controla o FPS do jogo
