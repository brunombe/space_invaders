from PPlay.sprite import *
from PPlay.keyboard import *
from PPlay.mouse import *
from invadedores import teclado, janela, mouse, clicou_em, tela, dificuldade, velocidade, keyboard



nave = Sprite("nave.png")
nave.set_position((janela.width/2-nave.width/2),(janela.height/2-nave.height/2) +220)

while True:
    if keyboard.key_pressed("right"):
        nave.x += velocidade
    if keyboard.key_pressed("left"):
        nave.x -= velocidade