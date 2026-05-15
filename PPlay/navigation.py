import heapq
import math

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

class Navigation:
    @staticmethod
    def heuristica(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    @classmethod
    def encontrar_caminho(cls, mapa, inicio_px, fim_px):
        tile = mapa.tamanho_tile
        # Converte pixels para índices da grade
        start = (int(inicio_px[0] // tile), int(inicio_px[1] // tile))
        goal = (int(fim_px[0] // tile), int(fim_px[1] // tile))
        
        largura = len(mapa.mapa_tiles[0])
        altura = len(mapa.mapa_tiles)
        
        # A* Core
        queue = [(0, start)]
        caminhos = {start: None}
        custos = {start: 0}
        
        while queue:
            atual = heapq.heappop(queue)[1]
            if atual == goal: break
            
            # Movimentos cardinais (cima, baixo, esquerda, direita)
            for dx, dy in [(0,1),(0,-1),(1,0),(-1,0)]:
                vizinho = (atual[0] + dx, atual[1] + dy)
                if 0 <= vizinho[0] < largura and 0 <= vizinho[1] < altura:
                    # Verifica se o tile é sólido
                    if mapa.mapa_tiles[vizinho[1]][vizinho[0]] is not None: continue
                    
                    novo_custo = custos[atual] + 1
                    if vizinho not in custos or novo_custo < custos[vizinho]:
                        custos[vizinho] = novo_custo
                        prioridade = novo_custo + cls.heuristica(vizinho, goal)
                        heapq.heappush(queue, (prioridade, vizinho))
                        caminhos[vizinho] = atual
        
        if goal not in caminhos: return []
        
        # Reconstrói caminho convertendo de volta para pixels (CENTRO DO TILE)
        percurso = []
        passo = goal
        offset = tile / 2 # Alvo é o centro do quadrado
        while passo is not None:
            percurso.append((passo[0] * tile + offset, passo[1] * tile + offset))
            passo = caminhos[passo]
        return percurso[::-1]