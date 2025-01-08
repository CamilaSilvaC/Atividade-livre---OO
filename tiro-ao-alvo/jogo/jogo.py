import pygame
import random
import sys
import json
import os
import Constants

# Classe que representa o estado do jogo
class GameState:
    def __init__(self):
        self.pontos = 0  # Pontos atuais do jogador
        self.timer = 1800  # Tempo restante do jogo em frames (30 segundos)
        self.recorde = 0  # Recorde de pontos
        self.game_paused = False  # Indica se o jogo está pausado
        self.finalizar = False  # Indica se o jogo deve finalizar
        self.tempo_acabou = False  # Indica se o tempo acabou

    def reset(self):
        # Reseta o estado do jogo para valores iniciais
        self.pontos = 0
        self.timer = 1800
        self.tempo_acabou = False

    def update(self):
        # Atualiza o estado do jogo, verificando se o tempo acabou
        if self.timer < 0:
            self.timer = 0
            if self.pontos > self.recorde:
                self.recorde = self.pontos
            self.tempo_acabou = True

    def save_to_json(self, filename):
        # Salva o estado atual do jogo em um arquivo JSON
        with open(filename, 'w') as file:
            json.dump(self.__dict__, file)

    def load_from_json(self, filename):
        # Carrega o estado do jogo a partir de um arquivo JSON
        with open(filename, 'r') as file:
            data = json.load(file)
            self.__dict__.update(data)

# Função para listar arquivos JSON disponíveis no diretório atual
def listar_arquivos_json():
    arquivos = [f for f in os.listdir('.') if f.endswith('.json')]
    if arquivos:
        print("Arquivos JSON disponíveis:")
        for arquivo in arquivos:
            print(f"- {arquivo}")
    else:
        print("Nenhum arquivo JSON disponível.")

# Menu interativo no terminal para iniciar ou carregar o jogo
def terminal_menu():
    print("Bem-vindo ao jogo Tiro ao Alvo!")
    print("1. Iniciar novo jogo")
    print("2. Carregar jogo salvo")
    print("3. Sair")
    choice = input("Escolha uma opção: ")

    if choice == '2':
        listar_arquivos_json()
        filename = input("Digite o nome do arquivo JSON: ")
        try:
            game_state.load_from_json(filename)
            print("Jogo carregado com sucesso!")
        except FileNotFoundError:
            print("Arquivo não encontrado. Iniciando novo jogo.")
    elif choice == '3':
        sys.exit()

# Classe que representa os alvos no jogo
class Alvo(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.image.load(Constants.ALVO).convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]

# Classe que representa a mira do jogador
class Mira(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(Constants.MIRA).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.sound = pygame.mixer.Sound(Constants.DISPARO)

    def update(self):
        # Atualiza a posição da mira para seguir o cursor do mouse
        self.rect.center = pygame.mouse.get_pos()

    def shoot(self, grupo_de_alvos):
        # Realiza um disparo e verifica se acertou algum alvo
        global game_state
        self.sound.play()
        colisions = pygame.sprite.spritecollide(self, grupo_de_alvos, False)
        for colision in colisions:
            game_state.pontos += 1
            colision.kill()
            alvo = Alvo(random.randrange(0, Constants.LARGURA), random.randrange(0, Constants.ALTURA))
            grupo_de_alvos.add(alvo)

# Função para exibir o menu inicial do jogo
def menu_inicial(screen, font):
    running = True
    while running:
        screen.fill((49, 102, 63))
        titulo = font.render("Bem-vindo ao jogo Tiro ao Alvo", True, (255, 255, 255))
        titulo_rect = titulo.get_rect(center=(Constants.LARGURA / 2, Constants.ALTURA / 2 - 70))
        screen.blit(titulo, titulo_rect)

        instrucao_font = pygame.font.Font(Constants.FONTE, 18)
        instrucao = instrucao_font.render("Clique em ENTER para iniciar", True, (255, 255, 255))
        instrucao_rect = instrucao.get_rect(center=(Constants.LARGURA / 2, Constants.ALTURA / 2 - 30))
        screen.blit(instrucao, instrucao_rect)

        pausa = instrucao_font.render("Pressione ESC para pausar o jogo", True, (255, 255, 255))
        pausa_rect = pausa.get_rect(center=(Constants.LARGURA / 2, Constants.ALTURA / 2 + 10))
        screen.blit(pausa, pausa_rect)

        salvar = instrucao_font.render("Pressione S para salvar o jogo", True, (255, 255, 255))
        salvar_rect = salvar.get_rect(center=(Constants.LARGURA / 2, Constants.ALTURA / 2 + 50))
        screen.blit(salvar, salvar_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = False

        pygame.display.flip()

# Função para exibir a tela de fim de jogo
def tela_fim_jogo(screen, font, recorde):
    running = True
    while running:
        screen.fill((49, 102, 63))
        fim_texto = font.render("Tempo Esgotado!", True, (255, 255, 255))
        fim_texto_rect = fim_texto.get_rect(center=(Constants.LARGURA / 2, Constants.ALTURA / 2 - 50))
        screen.blit(fim_texto, fim_texto_rect)

        recorde_texto = font.render(f"Recorde: {recorde}", True, (255, 255, 255))
        recorde_texto_rect = recorde_texto.get_rect(center=(Constants.LARGURA / 2, Constants.ALTURA / 2))
        screen.blit(recorde_texto, recorde_texto_rect)

        instrucao_font = pygame.font.Font(Constants.FONTE, 18)
        instrucao = instrucao_font.render("Pressione ENTER para jogar novamente", True, (255, 255, 255))
        instrucao_rect = instrucao.get_rect(center=(Constants.LARGURA / 2, Constants.ALTURA / 2 + 50))
        screen.blit(instrucao, instrucao_rect)

        salvar_instrucao = instrucao_font.render("Pressione S para salvar o jogo", True, (255, 255, 255))
        salvar_instrucao_rect = salvar_instrucao.get_rect(center=(Constants.LARGURA / 2, Constants.ALTURA / 2 + 90))
        screen.blit(salvar_instrucao, salvar_instrucao_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = False
                elif event.key == pygame.K_s:
                    filename = input("Digite o nome do arquivo para salvar (exemplo: estado_jogo.json): ")
                    game_state.save_to_json(filename)
                    print("Jogo salvo com sucesso!")

        pygame.display.flip()

# Inicialização do Pygame
pygame.init()

# Criação do estado inicial do jogo
game_state = GameState()
terminal_menu()

# Configuração da tela do jogo
screen = pygame.display.set_mode((Constants.LARGURA, Constants.ALTURA))
bg = pygame.image.load(Constants.BG).convert()
bg = pygame.transform.scale(bg, (Constants.LARGURA, Constants.ALTURA))
clock = pygame.time.Clock()
font = pygame.font.Font(Constants.FONTE, 25)
pygame.display.set_caption('Tiro ao alvo')
grupo_de_alvos = pygame.sprite.Group()
for i in range(20):
    alvo = Alvo(random.randrange(0, Constants.LARGURA), random.randrange(0, Constants.ALTURA))
    grupo_de_alvos.add(alvo)
mira = Mira()
mira_group = pygame.sprite.Group()
mira_group.add(mira)
menu_inicial(screen, font)

# Loop principal do jogo
while not game_state.finalizar:
    if game_state.tempo_acabou:
        tela_fim_jogo(screen, font, game_state.recorde)
        game_state.reset()
    elif not game_state.game_paused:
        pygame.mouse.set_visible(False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_state.game_paused = not game_state.game_paused
                elif event.key == pygame.K_s:
                    filename = input("Digite o nome do arquivo para salvar (exemplo: estado_jogo.json): ")
                    game_state.save_to_json(filename)
                    print("Jogo salvo com sucesso!")
            if event.type == pygame.MOUSEBUTTONDOWN:
                mira.shoot(grupo_de_alvos)
        screen.blit(bg, (0, 0))
        grupo_de_alvos.draw(screen)
        mira_group.draw(screen)
        mira_group.update()
        score = font.render(f'Pontos: {game_state.pontos}', True, (0, 0, 0))
        screen.blit(score, (50, 50))
        tempo = font.render(f'Tempo: {game_state.timer / 60:.1f} s', True, (0, 0, 0))
        screen.blit(tempo, (50, 100))
        game_state.timer -= 1
        game_state.update()
    else:
        screen.fill((104, 176, 123))
        pygame.mouse.set_visible(True)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_state.game_paused = not game_state.game_paused
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pause = font.render(f"PRECIONE ESC PARA INICIAR", True, (255, 255, 255))
        points = font.render(f"RECORDE: {game_state.recorde}", True, (255, 255, 255))
        pause_rect = pause.get_rect(center=(Constants.LARGURA / 2, Constants.ALTURA / 2))
        points_rect = points.get_rect(center=(Constants.LARGURA / 2, Constants.ALTURA / 2 - 50))
        screen.blit(pause, pause_rect)
        screen.blit(points, points_rect)
    pygame.display.flip()
    clock.tick(60)
