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

class InputManager:
    """
    Gerenciador de Ações. Permite mapear múltiplas teclas para uma única ação.
    """
    _mapa_acoes = {}

    @classmethod
    def define_action(cls, nome_acao, lista_teclas):
        """Mapeia um nome (ex: 'pulo') a várias teclas (ex: ['SPACE', 'UP', 'W'])."""
        cls._mapa_acoes[nome_acao] = lista_teclas

    @classmethod
    def is_active(cls, nome_acao):
        """Verifica se qualquer uma das teclas mapeadas para a ação está pressionada."""
        from .window import Window
        teclado = Window.get_instance().keyboard
        
        if nome_acao not in cls._mapa_acoes:
            return False
            
        for tecla in cls._mapa_acoes[nome_acao]:
            if teclado.key_pressed(tecla):
                return True
        return False

    @classmethod
    def action_pressed(cls, nome_acao):
        """Verifica se a ação foi disparada (apenas o primeiro frame)."""
        from .window import Window
        teclado = Window.get_instance().keyboard
        
        if nome_acao not in cls._mapa_acoes:
            return False
            
        for tecla in cls._mapa_acoes[nome_acao]:
            if teclado.key_down(tecla):
                return True
        return False