from PPlay.sprite import *
from PPlay.keyboard import *
from background import cor

keyboard = Keyboard()


def Jogatina(janela, nave, tiros, velocidade, velocidade_tiro):
    cor(janela, "vermelho")
    nave.draw()
    if keyboard.key_pressed("right"):
        nave.x += velocidade*janela.delta_time()
    if keyboard.key_pressed("left"):
        nave.x -= velocidade*janela.delta_time()
    if nave.x < 0:
        nave.x = 0
    if nave.x > janela.width - nave.width:
        nave.x = janela.width - nave.width
    if keyboard.key_down("space"):
        novo_tiro = Sprite("tiro.png")
        novo_tiro.set_position(nave.x + nave.width/2 - novo_tiro.width/2, nave.y - novo_tiro.height)
        tiros.append(novo_tiro)
    for tiro in tiros[:]:
        tiro.draw()
        tiro.y -= velocidade_tiro*janela.delta_time()
        if tiro.y < 0:
            tiros.remove(tiro)