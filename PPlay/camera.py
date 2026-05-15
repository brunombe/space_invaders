
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
class Camera:
    _instance = None

    def __init__(self, largura_janela, altura_janela):
        self.x = 0
        self.y = 0
        self.largura = largura_janela
        self.altura = altura_janela
        
        self.limite_topo = None
        self.limite_esquerda = None
        self.limite_base = None
        self.limite_direita = None

        Camera._instance = self

    @classmethod
    def get_instance(cls):
        return cls._instance

    def follow(self, target, suavizacao=0.1):
        """Centraliza a câmera no alvo."""
        # O alvo centralizado na tela
        alvo_x = (target.x + target.width / 2) - self.largura / 2
        alvo_y = (target.y + target.height / 2) - self.altura / 2

        # LERP (Movimento Suave)
        self.x += (alvo_x - self.x) * suavizacao
        self.y += (alvo_y - self.y) * suavizacao
        
        self._aplicar_limites()

    def set_world_bounds(self, largura_mundo, altura_mundo):
        self.limite_esquerda = 0
        self.limite_topo = 0
        self.limite_direita = largura_mundo - self.largura
        self.limite_base = altura_mundo - self.altura

    def _aplicar_limites(self):
        if self.limite_esquerda is not None:
            if self.x < self.limite_esquerda: self.x = self.limite_esquerda
            if self.x > self.limite_direita: self.x = self.limite_direita
            if self.y < self.limite_topo: self.y = self.limite_topo
            if self.y > self.limite_base: self.y = self.limite_base

    def transform_x(self, world_x):
        return world_x - self.x

    def transform_y(self, world_y):
        return world_y - self.y