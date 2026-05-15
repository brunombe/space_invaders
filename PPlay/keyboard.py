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

class Keyboard:
    def __init__(self):
        # Mapeamento estendido para facilitar a vida do aluno
        self.mapa = {
            "LEFT": pygame.K_LEFT, "RIGHT": pygame.K_RIGHT,
            "UP": pygame.K_UP, "DOWN": pygame.K_DOWN,
            "SPACE": pygame.K_SPACE, "ESC": pygame.K_ESCAPE,
            "ENTER": pygame.K_RETURN, "LSHIFT": pygame.K_LSHIFT
        }

    def _get_code(self, key):
        if isinstance(key, str):
            key = key.upper()
            if key in self.mapa:
                return self.mapa[key]
            return getattr(pygame, f"K_{key.lower()}", None)
        return key

    def key_pressed(self, key):
        """Verifica se a tecla está sendo segurada (Input contínuo)."""
        codigo = self._get_code(key)
        return pygame.key.get_pressed()[codigo] if codigo else False

    def key_down(self, key):
        """Verifica se a tecla foi apertada NESTE frame (Único)."""
        codigo = self._get_code(key)
        janela = Window.get_instance()
        for evento in janela.eventos:
            if evento.type == pygame.KEYDOWN and evento.key == codigo:
                return True
        return False

    def draw_debug(self, x=10, y=10):
        """Debug: Mostra teclas detectadas no frame."""
        janela = Window.get_instance()
        for evento in janela.eventos:
            if evento.type == pygame.KEYDOWN:
                janela.draw_text(f"Tecla: {pygame.key.name(evento.key)}", x, y, cor="red")