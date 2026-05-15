import pygame
import random
from .window import Window
from .camera import Camera

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

class ScreenEffects:
    """
    Efeitos de impacto visual: Tremer a tela, Flash de dano e Escuridão.
    """
    _shake_time = 0
    _shake_intensity = 0
    _flash_time = 0
    _flash_color = (255, 255, 255)

    @classmethod
    def shake(cls, intensidade=5, duracao=0.3):
        """Faz a tela tremer por X segundos."""
        cls._shake_intensity = intensidade
        cls._shake_time = duracao

    @classmethod
    def flash(cls, cor=(255, 255, 255), duracao=0.1):
        """Faz a tela piscar com uma cor (ex: vermelho para dano)."""
        cls._flash_color = cor
        cls._flash_time = duracao

    @classmethod
    def update(cls):
        """Atualiza os temporizadores dos efeitos."""
        dt = Window.get_instance().delta_time()
        if cls._shake_time > 0:
            cls._shake_time -= dt
        if cls._flash_time > 0:
            cls._flash_time -= dt

    @classmethod
    def apply_to_camera(cls):
        """Aplica o tremor na câmera atual."""
        cam = Camera.get_instance()
        if cam and cls._shake_time > 0:
            cam.x += random.uniform(-cls._shake_intensity, cls._shake_intensity)
            cam.y += random.uniform(-cls._shake_intensity, cls._shake_intensity)

    @classmethod
    def draw_flash(cls):
        """Desenha o overlay de flash se estiver ativo."""
        if cls._flash_time > 0:
            s = pygame.Surface((Window.get_instance().largura, Window.get_instance().altura))
            s.fill(cls._flash_color)
            s.set_alpha(150) # Transparência do flash
            Window.get_screen().blit(s, (0, 0))

class LightingSystem:
    """Cria atmosfera de escuridão com fontes de luz dinâmicas."""
    def __init__(self, opacidade_noite=240):
        self.opacidade = opacidade_noite
        self.fog = pygame.Surface((Window.get_instance().largura, Window.get_instance().altura))
        self.lights = [] 

    def draw(self):
        # Preenche a névoa com azul escuro/preto
        self.fog.fill((10, 10, 25)) 
        
        # 'Fura' a escuridão com as luzes
        for (lx, ly, raio, intensidade) in self.lights:
            cam = Camera.get_instance()
            tx = cam.transform_x(lx) if cam else lx
            ty = cam.transform_y(ly) if cam else ly
            
            # Superfície da luz com canal Alpha para degradê
            luz_surf = pygame.Surface((raio*2, raio*2), pygame.SRCALPHA)
            for r in range(raio, 0, -15):
                alpha = int(intensidade * (1 - r/raio))
                pygame.draw.circle(luz_surf, (255, 200, 100, alpha), (raio, raio), r)
            
            # Modo ADD faz as luzes se somarem se cruzarem
            self.fog.blit(luz_surf, (tx - raio, ty - raio), special_flags=pygame.BLEND_RGBA_ADD)
        
        # MULT escurece o que está embaixo mantendo a cor das luzes
        Window.get_screen().blit(self.fog, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        self.lights = []