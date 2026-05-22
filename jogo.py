from PPlay.sprite import *
from PPlay.keyboard import *
from background import cor

keyboard = Keyboard()

velocidade_inimigo = 100

def Jogatina(janela, nave, tiros, velocidade, velocidade_tiro, inimigos):
    global velocidade_inimigo
    
    cor(janela, "vermelho")
    nave.draw()

    dt = janela.delta_time()
    deslocamento_x = velocidade_inimigo * dt
    bateu_na_parede = False
    
    menor_x = janela.width
    maior_x = 0
    tem_inimigos = False
    
    for linha in inimigos:
        for bicho in linha:
            tem_inimigos = True
            if bicho.x < menor_x:
                menor_x = bicho.x
            if bicho.x + bicho.width > maior_x:
                maior_x = bicho.x + bicho.width
                
    if tem_inimigos:
        if menor_x + deslocamento_x <= 0 or maior_x + deslocamento_x >= janela.width:
            velocidade_inimigo *= -1                   
            deslocamento_x = velocidade_inimigo * dt  
            bateu_na_parede = True                     
            
        for linha in inimigos:
            for bicho in linha:
                bicho.x += deslocamento_x
                if bateu_na_parede:
                    bicho.y += 20 
                bicho.draw()

    if keyboard.key_pressed("right"):
        nave.x += velocidade * dt
    if keyboard.key_pressed("left"):
        nave.x -= velocidade * dt
        
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
        tiro.y -= velocidade_tiro * dt
        if tiro.y < 0:
            tiros.remove(tiro)