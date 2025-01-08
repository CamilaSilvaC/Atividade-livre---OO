
import os

# Diretório atual do arquivo Constants.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Caminhos relativos à pasta 'assets'
BG = os.path.join(BASE_DIR, '../assets/images/bg.webp')
FONTE = os.path.join(BASE_DIR, '../assets/fonts/PixelGameFont.ttf')
ALVO = os.path.join(BASE_DIR, '../assets/images/target.png')
MIRA = os.path.join(BASE_DIR, '../assets/images/mouse.png')
DISPARO = os.path.join(BASE_DIR, '../assets/audio/disparo.mp3')


#tamanho da tela
LARGURA = 1080
ALTURA = 620
