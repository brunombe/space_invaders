from PPlay.sprite import *
from PPlay.keyboard import *
from PPlay.mouse import *
# from rato import clicou_em

keyboard = Keyboard()
janela = Window(1200,600)
janela.set_background_color([15,0,20])
mouse = Mouse()

mouse_pressed_before = False

def clicou_em(obj):
    global mouse_pressed_before
    mouse_pressed_now = mouse.button_pressed(1)
    clicked = mouse.is_over_object(obj) and mouse_pressed_before and not mouse_pressed_now
    mouse_pressed_before = mouse_pressed_now
    return clicked

tela = 0
dificuldade = 0


start = Sprite("start.jpg")
start.set_position((janela.width/2-start.width/2),(janela.height/2-start.height/2))

dificult = Sprite("dificult.jpg")
dificult.set_position((janela.width/2-dificult.width/2),(janela.height/2-dificult.height/2) + 75)

ranking = Sprite("ranking.jpg")
ranking.set_position((janela.width/2-ranking.width/2),(janela.height/2-ranking.height/2) + 150)

exit = Sprite("exit.jpg")
exit.set_position((janela.width/2-exit.width/2),(janela.height/2-exit.height/2) +225)

facil = Sprite("facil.png")
facil.set_position((janela.width/2-facil.width/2),(janela.height/2-facil.height/2) +225)

medio = Sprite("medio.png")
medio.set_position((janela.width/2-medio.width/2),(janela.height/2-medio.height/2) + 150)

dificil = Sprite("dificil.png")
dificil.set_position((janela.width/2-dificil.width/2),(janela.height/2-dificil.height/2) +75)

nave = Sprite("nave.png")
nave.set_position((janela.width/2-nave.width/2),(janela.height/2-nave.height/2) +280)

tiro_sprite = Sprite("tiro.png")
tiros = []

while True:
    #velocidade nave
    if dificuldade == 0:
      velocidade = 500
    elif dificuldade == 1:
       velocidade = 400
    elif dificuldade == 2:
       velocidade = 300

    #velocidade tiro
    if dificuldade == 0:
        velocidade_tiro = 700
    elif dificuldade == 1:
        velocidade_tiro = 600
    elif dificuldade == 2:    
        velocidade_tiro = 500
    
    if tiros == []:
        tiro_status = False
    else:
        tiro_status = True
    #--------------------------------------------------------------------------------
    if tela == 0:
        start.draw()
        dificult.draw()
        ranking.draw()
        exit.draw()

        if clicou_em(start):
            tela = 1

        if clicou_em(dificult):
            tela = 2

        if clicou_em(ranking):
            tela = 3

        if clicou_em(exit):
            break

        
    if tela == 1:
        janela.set_background_color([200,0,20])
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


    if tela == 2:
        facil.draw()
        medio.draw()
        dificil.draw()
        if clicou_em(facil):
            dificuldade = 0
        if clicou_em(medio):
            dificuldade = 1
        if clicou_em(dificil):
            dificuldade = 2

    if tela == 3:
        tela = 0 
    janela.update()