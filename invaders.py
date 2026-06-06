from PPlay.sprite import *
from PPlay.keyboard import *
from PPlay.mouse import *
from jogo import Jogatina
from sprites import bichinhos
from background import cor

def clicou_em(obj):
    return mouse.button_down(1) and mouse.is_over_object(obj)

keyboard = Keyboard()
janela = Window(1200,600)
mouse = Mouse()

#Cria os sprites
sprites = bichinhos(janela)
start   = sprites["start"]
dificult = sprites["dificult"]
ranking  = sprites["ranking"]
exit     = sprites["exit"]
facil    = sprites["facil"]
medio    = sprites["medio"]
dificil  = sprites["dificil"]
nave     = sprites["nave"]
bicho    = sprites["bicho"]
inimigos  = sprites["inimigos"]

dificuldade = 0
tiro_sprite = Sprite("tiro.png")
tiros = []
tiros_inimigos = []
vidas = 3
invencivel = False
tempo_invencivel = 0
tempo_ultimo_tiro = 0
tela = 0

fps_real = 0
fps_calculo = 0

#--------------------------------------------------------------------------------
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
    
    if tela == 0:
        cor(janela, "roxinho")
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
            
    elif tela == 1:
        tela, vidas, invencivel, tempo_invencivel, tempo_ultimo_tiro = Jogatina(
            janela, nave, tiros, tiros_inimigos, velocidade, velocidade_tiro, inimigos,
            vidas, invencivel, tempo_invencivel, tempo_ultimo_tiro
        )
        
        if keyboard.key_pressed("ESC") or bicho.y > janela.height - 100 or tela == 0:
            tela = 0
            sprites = bichinhos(janela) 
            inimigos = sprites["inimigos"]
            nave = sprites["nave"]
            tiros.clear()
            tiros_inimigos.clear()
            vidas = 3
            invencivel = False
            tempo_invencivel = 0
            tempo_ultimo_tiro = 0

    elif tela == 2:
        cor(janela, "cinza")
        facil.draw()
        medio.draw()
        dificil.draw()
        if clicou_em(facil):
            dificuldade = 0
            tela = 0
        if clicou_em(medio):
            dificuldade = 1
            tela = 0
        if clicou_em(dificil):
            dificuldade = 2
            tela = 0

    elif tela == 3:
        tela = 0 
        
    janela.update()