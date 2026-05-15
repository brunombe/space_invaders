from .animation import Animation
from .window import Window

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

class Sprite(Animation):
    def __init__(self, caminho_imagem, total_frames=1):
        super().__init__(caminho_imagem, total_frames)
        self.vx = 0
        self.vy = 0
        self.no_chao = False
        self.body = None

    # MÉTODOS TRADICIONAIS (Mantidos)
    def move_key_x(self, velocidade):
        janela = Window.get_instance()
        teclado = janela.keyboard
        dt = janela.delta_time()
        if teclado.key_pressed("left"): self.x -= velocidade * dt
        if teclado.key_pressed("right"): self.x += velocidade * dt

    def move_key_y(self, velocidade):
        janela = Window.get_instance()
        teclado = janela.keyboard
        dt = janela.delta_time()
        if teclado.key_pressed("up"): self.y -= velocidade * dt
        if teclado.key_pressed("down"): self.y += velocidade * dt

    def move_x(self, velocidade):
        self.x += velocidade * Window.get_instance().delta_time()

    def move_y(self, velocidade):
        self.y += velocidade * Window.get_instance().delta_time()

    def pular(self, forca_pulo):
        """Impulso manual (Use apenas se não usar o update_physics)."""
        if self.no_chao:
            self.vy = -forca_pulo
            self.no_chao = False

    # SISTEMA DE FÍSICA CINEMÁTICA
    def setup_physics(self, engine):
        from .physics import KinematicBody
        self.body = KinematicBody(self, engine)

    def update_physics(self, lista_solidos):
        if self.body:
            # O KinematicBody agora gerencia inércia, pulo e colisão
            self.body.update(lista_solidos)
        else:
            # Se não houver física pro, apenas atualiza animação
            self.update()
        
        # Sincroniza animação (herança de Animation)
        self.update()