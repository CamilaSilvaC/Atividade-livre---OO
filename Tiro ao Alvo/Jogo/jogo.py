import pygame  
import random
import sys 
import Constants

class GameState:
    def __init__(self):
        self.pontos = 0
        self.timer = 1800  # 30 segundos
        self.recorde = 0
        self.game_paused = False
        self.finalizar = False
    
    def reset(self):
        self.pontos = 0
        self.timer = 1800  # Reinicia o tempo
    
    def update(self):
        if self.timer < 0:
            self.timer = 1800
            if self.pontos > self.recorde:
                self.recorde = self.pontos
            self.reset()
            self.game_paused = not self.game_paused


class Alvo(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.image.load(Constants.ALVO).convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]


class Mira(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(Constants.MIRA).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.sound = pygame.mixer.Sound(Constants.DISPARO)
    
    def update(self):
        self.rect.center = pygame.mouse.get_pos()

    def shoot(self, grupo_de_alvos):
        global game_state
        self.sound.play()

        colisions = pygame.sprite.spritecollide(self, grupo_de_alvos, False)
        for colision in colisions:
            game_state.pontos += 1
            colision.kill()
            alvo = Alvo(random.randrange(0, Constants.LARGURA), random.randrange(0, Constants.ALTURA))
            grupo_de_alvos.add(alvo)


pygame.init()

# Definindo o estado do jogo
game_state = GameState()

screen = pygame.display.set_mode((Constants.LARGURA, Constants.ALTURA))

# Imagem de background
bg = pygame.image.load(Constants.BG).convert()
bg = pygame.transform.scale(bg, (Constants.LARGURA, Constants.ALTURA))

clock = pygame.time.Clock()

font = pygame.font.Font(Constants.FONTE, 25)

pygame.display.set_caption('Tiro ao alvo')

grupo_de_alvos = pygame.sprite.Group()

# Criando os alvos
for i in range(20):
    alvo = Alvo(random.randrange(0, Constants.LARGURA), random.randrange(0, Constants.ALTURA))
    grupo_de_alvos.add(alvo)

mira = Mira()
mira_group = pygame.sprite.Group()
mira_group.add(mira)

while not game_state.finalizar:
    if not game_state.game_paused:
        pygame.mouse.set_visible(False)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # ESC para pausar
                    game_state.game_paused = not game_state.game_paused
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mira.shoot(grupo_de_alvos)

        # Atualizando o jogo
        screen.blit(bg, (0, 0))
        grupo_de_alvos.draw(screen)
        mira_group.draw(screen)
        mira_group.update()

        # Exibindo pontos e tempo
        score = font.render(f'Pontos: {game_state.pontos}', True, (0, 0, 0))
        screen.blit(score, (50, 50))

        tempo = font.render(f'Tempo: {game_state.timer / 60:.1f} s', True, (0, 0, 0))
        screen.blit(tempo, (50, 100))

        # Diminuindo o tempo
        game_state.timer -= 1
        
        # Atualizando o estado do jogo
        game_state.update()

    else:
        # Tela de pausa
        screen.fill((252, 132, 3))
        pygame.mouse.set_visible(True)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # ESC para voltar
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
