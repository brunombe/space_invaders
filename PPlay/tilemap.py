import pygame
from .sprite import Sprite
from .camera import Camera
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

class TileMap:
    """
    Carrega e gerencia um mapa baseado em uma grade (grid) de um arquivo .txt.
    """
    def __init__(self, tamanho_tile):
        self.tamanho_tile = tamanho_tile
        self.mapa_tiles = [] # Matriz de objetos Sprite
        self.tiles_colidiveis = [] # Lista apenas dos que bloqueiam movimento
        
        self.largura_mapa_px = 0
        self.altura_mapa_px = 0

    def carregar_mapa(self, caminho_txt, mapeamento):
        """
        Lê o arquivo .txt e cria os Sprites.
        mapeamento: dicionário {'#': 'chao.png', '@': 'parede.png', 'solido': ['#', '@']}
        """
        self.mapa_tiles = []
        self.tiles_colidiveis = []
        
        try:
            with open(caminho_txt, 'r') as f:
                linhas = f.readlines()
        except FileNotFoundError:
            print(f"ERRO: Arquivo de mapa {caminho_txt} não encontrado.")
            return

        for linha_idx, linha in enumerate(linhas):
            linha_objetos = []
            for col_idx, char in enumerate(linha.strip()):
                if char in mapeamento:
                    # Cria o tile na posição correta do grid
                    tile = Sprite(mapeamento[char], 1)
                    px = col_idx * self.tamanho_tile
                    py = linha_idx * self.tamanho_tile
                    tile.set_position(px, py)
                    
                    linha_objetos.append(tile)
                    
                    # Se o caractere estiver na lista de 'solidos' do mapeamento
                    if 'solido' in mapeamento and char in mapeamento['solido']:
                        self.tiles_colidiveis.append(tile)
                else:
                    linha_objetos.append(None) # Espaço vazio
            
            self.mapa_tiles.append(linha_objetos)

        # Calcula o tamanho total do mundo para a câmera
        self.altura_mapa_px = len(self.mapa_tiles) * self.tamanho_tile
        if len(self.mapa_tiles) > 0:
            self.largura_mapa_px = len(self.mapa_tiles[0]) * self.tamanho_tile
            
        # Ajusta a câmera automaticamente se ela existir
        if Camera.get_instance():
            Camera.get_instance().set_world_bounds(self.largura_mapa_px, self.altura_mapa_px)

    def draw(self):
        """
        Desenha apenas os tiles que estão visíveis na tela (Culling).
        Isso permite mapas gigantes com performance máxima.
        """
        cam = Camera.get_instance()
        if not cam:
            # Se não houver câmera, desenha tudo (não recomendado para mapas grandes)
            for linha in self.mapa_tiles:
                for tile in linha:
                    if tile: tile.draw()
            return

        # OTIMIZAÇÃO: Descobre quais índices do grid estão na tela
        inicio_col = max(0, int(cam.x // self.tamanho_tile))
        fim_col = min(len(self.mapa_tiles[0]), int((cam.x + cam.largura) // self.tamanho_tile) + 1)
        
        inicio_linha = max(0, int(cam.y // self.tamanho_tile))
        fim_linha = min(len(self.mapa_tiles), int((cam.y + cam.altura) // self.tamanho_tile) + 1)

        # Desenha apenas o que é necessário
        for r in range(inicio_linha, fim_linha):
            for c in range(inicio_col, fim_col):
                tile = self.mapa_tiles[r][c]
                if tile:
                    tile.draw()

    def get_solidos(self):
        """Retorna a lista de tiles que possuem colisão."""
        return self.tiles_colidiveis