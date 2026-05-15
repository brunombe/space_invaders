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

class Task:
    def __init__(self, delay, funcao, repetir, args):
        self.delay = delay
        self.tempo_restante = delay
        self.funcao = funcao
        self.repetir = repetir
        self.args = args
        self.finalizada = False

class Timer:
    """
    Gerenciador de tarefas agendadas. 
    Substitui a criação de variáveis de controle de tempo manuais.
    """
    _tasks = []

    @classmethod
    def after(cls, segundos, funcao, *args):
        """Executa uma função após X segundos."""
        cls._tasks.append(Task(segundos, funcao, False, args))

    @classmethod
    def every(cls, segundos, funcao, *args):
        """Executa uma função repetidamente a cada X segundos."""
        cls._tasks.append(Task(segundos, funcao, True, args))

    @classmethod
    def update(cls):
        """Processa todas as tarefas agendadas. Deve ser chamado no loop principal."""
        from .window import Window
        dt = Window.get_instance().delta_time()
        
        for task in cls._tasks[:]:
            task.tempo_restante -= dt
            if task.tempo_restante <= 0:
                task.funcao(*task.args)
                if task.repetir:
                    task.tempo_restante = task.delay
                else:
                    task.finalizada = True
                    cls._tasks.remove(task)