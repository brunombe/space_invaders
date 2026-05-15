import pygame
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

class Mouse:
    LEFT = 1
    MIDDLE = 2
    RIGHT = 3

    def get_position(self):
        """Retorna a posição do mouse corrigida para a escala do jogo."""
        janela = Window.get_instance()
        mx, my = pygame.mouse.get_pos()
        # Traduz os pixels da janela real para os pixels do jogo virtual
        return janela.screen_to_virtual_coords(mx, my)

    def button_pressed(self, button):
        return pygame.mouse.get_pressed()[button - 1]

    def button_down(self, button):
        janela = Window.get_instance()
        for evento in janela.eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == button:
                return True
        return False

    def is_over_object(self, obj):
        mx, my = self.get_position()
        return (obj.x <= mx <= obj.x + obj.width and 
                obj.y <= my <= obj.y + obj.height)

    def draw_debug(self):
        mx, my = self.get_position()
        janela = Window.get_instance()
        # O debug também deve usar a posição virtual para desenhar no lugar certo
        janela.draw_text(f"Mouse Virtual: ({int(mx)}, {int(my)})", mx+10, my-10, tamanho=14, cor="green")