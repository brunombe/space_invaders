import pygame
from .window import Window
from .camera import Camera
from .gameimage import GameImage

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

class ParallaxLayer:
    """
    Representa uma única camada do fundo com sua própria velocidade de scroll.
    """
    def __init__(self, caminho_imagem, fator_velocidade):
        # Carrega a imagem usando o sistema de Cache da GameImage
        self.sprite = GameImage(caminho_imagem)
        self.largura = self.sprite.width
        self.altura = self.sprite.height
        
        # Fator de velocidade: 0.0 (estático) a 1.0 (velocidade da câmera)
        self.fator = fator_velocidade

    def draw(self):
        janela = Window.get_instance()
        cam = Camera.get_instance()
        screen = Window.get_screen()
        
        if not cam:
            self.sprite.draw()
            return

        # Calcula o deslocamento (offset) baseado na câmera e no fator
        # O operador % garante que o fundo seja infinito
        deslocamento_x = (cam.x * self.fator) % self.largura
        
        # Desenha a primeira parte da imagem
        pos_x1 = -deslocamento_x
        screen.blit(self.sprite.image, (pos_x1, 0))
        
        # Desenha a segunda parte para preencher o vazio da repetição
        if pos_x1 < 0:
            screen.blit(self.sprite.image, (pos_x1 + self.largura, 0))

class ParallaxSystem:
    """
    Gerenciador de múltiplas camadas de Parallax.
    Organiza as camadas da mais distante para a mais próxima.
    """
    def __init__(self):
        self.camadas = []

    def add_layer(self, caminho_imagem, fator_velocidade):
        """
        Adiciona uma camada ao fundo. 
        Fatores menores (0.1, 0.2) para o que está longe.
        Fatores maiores (0.8, 0.9) para o que está perto.
        """
        nova_camada = ParallaxLayer(caminho_imagem, fator_velocidade)
        self.camadas.append(nova_camada)

    def draw(self):
        """Desenha todas as camadas na ordem em que foram adicionadas."""
        for camada in self.camadas:
            camada.draw()