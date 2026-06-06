import random
from PPlay.sprite import *
from PPlay.keyboard import *
from background import cor
from PPlay.collision import *

keyboard = Keyboard()
velocidade_inimigo = 100

def Jogatina(janela, nave, tiros, tiros_inimigos, velocidade, velocidade_tiro, inimigos, vidas, invencivel, tempo_invencivel, tempo_ultimo_tiro):
    global velocidade_inimigo
    
    cor(janela, "vermelho")
    dt = janela.delta_time()
    
    # ---------------------------------------------------------
    # 1. EFEITO DE PISCAR E INVENCIBILIDADE DO PLAYER
    # ---------------------------------------------------------
    visivel = True
    if invencivel:
        tempo_invencivel -= dt
        if tempo_invencivel <= 0:
            invencivel = False
        else:
            # Alterna a visibilidade multiplicando o tempo para criar o efeito "piscando"
            if int(tempo_invencivel * 10) % 2 == 0:
                visivel = False

    if visivel:
        nave.draw()

    # ---------------------------------------------------------
    # MOVIMENTAÇÃO DOS INIMIGOS (Seu código original)
    # ---------------------------------------------------------
    deslocamento_x = velocidade_inimigo * dt
    bateu_na_parede = False
    
    menor_x = janela.width
    maior_x = 0
    menor_y = janela.height if hasattr(janela, 'height') else 9999
    maior_y = 0
    
    tem_inimigos = False
    inimigos_vivos = [] # Usado para sortear qual monstro vai atirar
    
    for linha in inimigos:
        for bicho in linha:
            tem_inimigos = True
            inimigos_vivos.append(bicho)
            if bicho.x < menor_x: menor_x = bicho.x
            if bicho.x + bicho.width > maior_x: maior_x = bicho.x + bicho.width
            if bicho.y < menor_y: menor_y = bicho.y
            if bicho.y + bicho.height > maior_y: maior_y = bicho.y + bicho.height
                
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

        # Colisão: Tiros do player nos inimigos
        for tiro in tiros[:]:
            if (tiro.x + tiro.width >= menor_x and tiro.x <= maior_x and
                tiro.y + tiro.height >= menor_y and tiro.y <= maior_y):
                
                bateu = False
                for linha in reversed(inimigos):
                    for bicho in linha[:]:
                        if (tiro.x < bicho.x + bicho.width and
                            tiro.x + tiro.width > bicho.x and
                            tiro.y < bicho.y + bicho.height and
                            tiro.y + tiro.height > bicho.y):
                                linha.remove(bicho)
                                tiros.remove(tiro)
                                bateu = True
                                break
                    if bateu:
                        break

        # ---------------------------------------------------------
        # 2. LÓGICA DE TIRO DOS MONSTROS
        # ---------------------------------------------------------
        tempo_ultimo_tiro += dt
        # Tempo de recarga base (1 seg) + valor aleatório (entre 0 e 1.5 seg)
        limite_recarga = 1.0 + random.uniform(0.0, 1.5) 
        
        if tempo_ultimo_tiro > limite_recarga:
            tempo_ultimo_tiro = 0
            atirador = random.choice(inimigos_vivos)
            novo_tiro = Sprite("tiro.png") # Utilizando a mesma imagem de tiro
            novo_tiro.set_position(atirador.x + atirador.width/2 - novo_tiro.width/2, atirador.y + atirador.height)
            tiros_inimigos.append(novo_tiro)

    # ---------------------------------------------------------
    # 3. ATUALIZAÇÃO E COLISÃO DOS TIROS INIMIGOS
    # ---------------------------------------------------------
    for t_ini in tiros_inimigos[:]:
        t_ini.draw()
        t_ini.y += velocidade_tiro * dt
        
        # Remove o tiro se sair da tela
        if t_ini.y > janela.height:
            tiros_inimigos.remove(t_ini)
            
        # Checa colisão com o player (apenas se NÃO estiver invencível)
        elif not invencivel:
            if (t_ini.x < nave.x + nave.width and
                t_ini.x + t_ini.width > nave.x and
                t_ini.y < nave.y + nave.height and
                t_ini.y + t_ini.height > nave.y):
                
                vidas -= 1
                tiros_inimigos.clear()
                tiros.clear()
                
                # Reseta a nave para o centro (posição original ajustada para baixo)
                nave.set_position((janela.width/2 - nave.width/2), (janela.height/2 - nave.height/2) + 280)
                
                if vidas > 0:
                    invencivel = True
                    tempo_invencivel = 2.0 # Fica invencível por 2 segundos
                break

    # Se as vidas zerarem, sinaliza para retornar ao menu
    if vidas <= 0:
        return 0, vidas, invencivel, tempo_invencivel, tempo_ultimo_tiro

    # ---------------------------------------------------------
    # MOVIMENTAÇÃO E DISPARO DO PLAYER (Seu código original)
    # ---------------------------------------------------------
    if keyboard.key_pressed("right"): nave.x += velocidade * dt
    if keyboard.key_pressed("left"): nave.x -= velocidade * dt
        
    if nave.x < 0: nave.x = 0
    if nave.x > janela.width - nave.width: nave.x = janela.width - nave.width
        
    if keyboard.key_down("space"):
        novo_tiro = Sprite("tiro.png")
        novo_tiro.set_position(nave.x + nave.width/2 - novo_tiro.width/2, nave.y - novo_tiro.height)
        tiros.append(novo_tiro)
    
    for tiro in tiros[:]:
        tiro.draw()
        tiro.y -= velocidade_tiro * dt
        if tiro.y < 0:
            tiros.remove(tiro)

    # Retorna o estado atualizado do jogo (tela 1 = jogo rodando)
    return 1, vidas, invencivel, tempo_invencivel, tempo_ultimo_tiro