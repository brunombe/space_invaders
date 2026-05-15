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

class ObjectGroup:
    """
    Organizador de objetos para facilitar a vida de quem não domina listas/POO.
    Funciona como uma 'camada' ou 'container' de sprites.
    """
    def __init__(self):
        self._objetos = []

    def add(self, *objetos):
        """Adiciona um ou mais objetos ao grupo."""
        for obj in objetos:
            if obj not in self._objetos:
                self._objetos.append(obj)

    def remove(self, obj):
        """Remove um objeto específico do grupo."""
        if obj in self._objetos:
            self._objetos.remove(obj)

    def update(self):
        """Chama o update() de todos os objetos que possuem esse método."""
        for obj in self._objetos:
            if hasattr(obj, "update"):
                obj.update()

    def update_physics(self, lista_solidos):
        """Aplica física em massa para todos os membros do grupo."""
        for obj in self._objetos:
            if hasattr(obj, "update_physics"):
                obj.update_physics(lista_solidos)

    def draw(self):
        """Desenha todos os objetos do grupo na tela."""
        for obj in self._objetos:
            if hasattr(obj, "draw"):
                obj.draw()

    def collided(self, alvo):
        """
        Verifica se o 'alvo' colidiu com QUALQUER objeto do grupo.
        Retorna o objeto do grupo que sofreu a colisão, ou None.
        """
        for obj in self._objetos:
            if alvo.collided(obj):
                return obj
        return None

    def empty(self):
        """Limpa todos os objetos do grupo."""
        self._objetos = []

    def __len__(self):
        return len(self._objetos)

    def get_all(self):
        """Retorna a lista bruta de objetos (para loops customizados)."""
        return self._objetos