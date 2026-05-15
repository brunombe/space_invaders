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

class Scene:
    """
    Classe base para todas as cenas do jogo.
    O aluno deve herdar desta classe para criar seus menus e fases.
    """
    def __init__(self):
        # Referência rápida para a janela e inputs
        from .window import Window
        self.janela = Window.get_instance()
        self.teclado = self.janela.keyboard
        self.mouse = self.janela.mouse

    def loop(self):
        """Onde o aluno coloca a lógica de movimento e física."""
        pass

    def draw(self):
        """Onde o aluno coloca os comandos de desenho."""
        pass

class SceneManager:
    """
    Controlador central que decide qual cena está ativa no momento.
    """
    _current_scene = None

    @classmethod
    def change_scene(cls, next_scene):
        """
        Troca a cena atual. 
        next_scene deve ser uma instância de uma classe que herda de Scene.
        """
        cls._current_scene = next_scene

    @classmethod
    def run(cls):
        """
        Executa o ciclo de vida da cena atual.
        Deve ser chamado dentro do loop principal do jogo.
        """
        if cls._current_scene:
            # 1. Executa a lógica da cena
            cls._current_scene.loop()
            
            # 2. Executa os desenhos da cena
            cls._current_scene.draw()
        else:
            from .window import Window
            Window.get_screen().fill((255, 0, 0)) # Alerta visual: Nenhuma cena ativa