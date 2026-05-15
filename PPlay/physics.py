import pygame
import math

"""
===============================================================================
POWER PPLAY 2.0 - Framework de Alta Performance para Desenvolvimento de Jogos
===============================================================================
Desenvolvedor Líder e Arquiteto da Versão 2.0: 
    Kauã Neves Jesus de Paula

Ano de Lançamento: 2026
Instituição: Universidade Federal Fluminense (IC-UFF) - Niterói, RJ
-------------------------------------------------------------------------------
Este software é uma evolução profunda e modernização da biblioteca PPlay,
originalmente concebida pela Equipe PPlay:
    Prof. Esteban Clua, Prof. Anselmo Montenegro, Gabriel Saldanha,
    Adônis Gasiglia, Yuri Nogueira e Sergio Herman.
===============================================================================
"""

class Physics:
    """
    MOTOR DE FÍSICA CINEMÁTICA 4.5 - THE FEELING UPDATE.
    """
    def __init__(self, gravidade=2500, vel_terminal=1500):
        self.gravidade = gravidade
        self.vel_terminal = vel_terminal
        self.SKIN = 0.1 # Aumentado levemente para estabilidade
        self.PASSO_MINIMO = 1.0 

    def processar_movimento(self, objeto, lista_solidos):
        from .window import Window
        dt = Window.get_instance().delta_time()

        # 1. Gravidade
        objeto.vy += self.gravidade * dt
        if objeto.vy > self.vel_terminal:
            objeto.vy = self.vel_terminal

        # 2. Deslocamentos
        dx = objeto.vx * dt
        dy = objeto.vy * dt

        # --- EIXO X (Horizontal) ---
        passos_x = int(abs(dx) / self.PASSO_MINIMO) + 1
        dist_por_passo_x = dx / passos_x

        for _ in range(passos_x):
            proximo_x = objeto.x + dist_por_passo_x
            rect_futuro = pygame.Rect(proximo_x, objeto.y, objeto.width, objeto.height)
            
            colidiu = False
            for solido in lista_solidos:
                if rect_futuro.colliderect(pygame.Rect(solido.x, solido.y, solido.width, solido.height)):
                    colidiu = True
                    if dist_por_passo_x > 0: objeto.x = solido.x - objeto.width - self.SKIN
                    else: objeto.x = solido.x + solido.width + self.SKIN
                    objeto.vx = 0
                    break
            if colidiu: break
            else: objeto.x = proximo_x

        # --- EIXO Y (Vertical) ---
        passos_y = int(abs(dy) / self.PASSO_MINIMO) + 1
        dist_por_passo_y = dy / passos_y
        
        objeto.no_chao = False
        for _ in range(passos_y):
            proximo_y = objeto.y + dist_por_passo_y
            rect_futuro = pygame.Rect(objeto.x, proximo_y, objeto.width, objeto.height)
            
            colidiu = False
            for solido in lista_solidos:
                if rect_futuro.colliderect(pygame.Rect(solido.x, solido.y, solido.width, solido.height)):
                    colidiu = True
                    if dist_por_passo_y > 0: # Caindo (Chão)
                        objeto.y = solido.y - objeto.height - self.SKIN
                        objeto.vy = 0
                        objeto.no_chao = True
                    else: # Teto
                        objeto.y = solido.y + solido.height + self.SKIN
                        objeto.vy = 0
                    break
            if colidiu: break
            else: objeto.y = proximo_y

class KinematicBody:
    """Componente Pro: Gerencia inércia e 'Input Buffering' para pulos perfeitos."""
    def __init__(self, sprite, physics_engine):
        self.sprite = sprite
        self.engine = physics_engine
        
        # Configurações de Movimento
        self.accel = 4500
        self.friccao = 0.2
        self.pulo = 950
        self.max_vel_x = 420

        # --- JUMP FEELING (A MÁGICA) ---
        self.coyote_timer = 0
        self.coyote_max = 0.15 # 150ms de tolerância após sair da plataforma
        
        self.jump_buffer_timer = 0
        self.jump_buffer_max = 0.15 # 150ms de memória para o botão de pulo

    def update(self, lista_solidos):
        from .window import Window
        janela = Window.get_instance()
        teclado = janela.keyboard
        dt = janela.delta_time()

        # 1. Movimento Horizontal
        dir = 0
        if teclado.key_pressed("left"): dir = -1
        if teclado.key_pressed("right"): dir = 1
        
        if dir != 0:
            self.sprite.vx += dir * self.accel * dt
        else:
            self.sprite.vx *= (1 - self.friccao)

        if abs(self.sprite.vx) > self.max_vel_x:
            self.sprite.vx = self.max_vel_x * (1 if self.sprite.vx > 0 else -1)

        # 2. Lógica de Pulo com Tolerância (Coyote Time & Buffer)
        
        # Update Coyote Timer (Tempo no chão)
        if self.sprite.no_chao:
            self.coyote_timer = self.coyote_max
        else:
            self.coyote_timer -= dt

        # Update Jump Buffer (Memória do botão)
        if teclado.key_down("space") or teclado.key_down("up"):
            self.jump_buffer_timer = self.jump_buffer_max
        else:
            self.jump_buffer_timer -= dt

        # Executa o pulo se ambas as condições de satisfação forem atendidas
        if self.jump_buffer_timer > 0 and self.coyote_timer > 0:
            self.sprite.vy = -self.pulo
            self.sprite.no_chao = False
            self.coyote_timer = 0       # Consome a tolerância
            self.jump_buffer_timer = 0  # Consome o buffer
            
        # Pulo Variável (Soltar o botão corta a subida - opcional)
        if not (teclado.key_pressed("space") or teclado.key_pressed("up")) and self.sprite.vy < -300:
            self.sprite.vy = -300

        # 3. Processar a Física
        self.engine.processar_movimento(self.sprite, lista_solidos)