import pygame

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

class GameObject:
    """
    A classe mais básica da engine. Representa qualquer 'coisa' que 
    tenha uma posição e um tamanho no mundo do jogo.
    """
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.scale_x = 1.0
        self.scale_y = 1.0
        self.rotation = 0.0
        self.transparency = 255
        
    def collided(self, outro_obj):
        """
        Verifica colisão básica (AABB - Axis-Aligned Bounding Box).
        É o método de colisão mais rápido que existe.
        """
        if (self.x < outro_obj.x + outro_obj.width and
            self.x + self.width > outro_obj.x and
            self.y < outro_obj.y + outro_obj.height and
            self.y + self.height > outro_obj.y):
            return True
        return False

    def set_position(self, x, y):
        """Define a posição do objeto no plano cartesiano."""
        self.x = x
        self.y = y
    
    def get_position(self):
        """Retorna a tupla (x, y) da posição atual."""
        return (self.x, self.y)
    
    def set_scale(self, escala_x, escala_y=None):
        """Define a escala horizontal e vertical. Se escala_y for None, usa escala_x."""
        self.scale_x = escala_x
        self.scale_y = escala_y if escala_y is not None else escala_x
    
    def get_scale(self):
        """Retorna a tupla (escala_x, escala_y) da escala atual."""
        return (self.scale_x, self.scale_y)
    
    def set_rotation(self, angulo):
        """Define o ângulo de rotação em graus."""
        self.rotation = angulo
    
    def get_rotation(self):
        """Retorna o ângulo de rotação atual."""
        return self.rotation
    
    def set_transparency(self, alfa):
        """Define o nível de transparência (0 a 255)."""
        self.transparency = max(0, min(255, alfa))
    
    def get_transparency(self):
        """Retorna o nível de transparência atual."""
        return self.transparency