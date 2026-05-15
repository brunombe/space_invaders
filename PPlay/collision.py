import pygame
import math
from .point import Point

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

class Collision:
    """
    Classe utilitária para detecção de colisões entre GameObjects.
    Oferece métodos desde o mais rápido (Retângulos) até o mais preciso (Pixels).
    """

    @staticmethod
    def collided(obj1, obj2):
        """
        O método mais rápido (AABB). 
        Verifica se os retângulos dos objetos se sobrepõem.
        """
        return (obj1.x < obj2.x + obj2.width and
                obj1.x + obj1.width > obj2.x and
                obj1.y < obj2.y + obj2.height and
                obj1.y + obj1.height > obj2.y)

    @staticmethod
    def collided_circle(obj1, obj2):
        """
        Verifica colisão entre dois círculos usando a distância entre centros.
        Assume que o raio é metade da largura do objeto.
        """
        # Calcula os centros
        raio1 = obj1.width / 2
        raio2 = obj2.width / 2
        
        centro1_x = obj1.x + raio1
        centro1_y = obj1.y + raio1
        centro2_x = obj2.x + raio2
        centro2_y = obj2.y + raio2
        
        # Teorema de Pitágoras: a² + b² = c²
        distancia = math.sqrt((centro2_x - centro1_x)**2 + (centro2_y - centro1_y)**2)
        
        return distancia < (raio1 + raio2)

    @staticmethod
    def perfect_collision(obj1, obj2):
        """
        Colisão por Máscara (Pixel Perfect). 
        Só ocorre se os pixels não transparentes se tocarem.
        Nota: Requer que os objetos sejam GameImage ou Sprites.
        """
        # Primeiro fazemos o check de retângulo (AABB) por performance.
        # Se os retângulos nem se tocam, é impossível os pixels se tocarem.
        if not Collision.collided(obj1, obj2):
            return False

        # Gera máscaras de bits a partir das imagens (o Pygame faz o cache interno)
        mask1 = pygame.mask.from_surface(obj1.image)
        mask2 = pygame.mask.from_surface(obj2.image)

        # Calcula a diferença de posição entre eles
        offset_x = int(obj2.x - obj1.x)
        offset_y = int(obj2.y - obj1.y)

        # Verifica se as máscaras se sobrepõem
        return mask1.overlap(mask2, (offset_x, offset_y)) is not None


    @staticmethod
    def raycast(origem_x, origem_y, destino_x, destino_y, lista_solidos):
        """
        Lança um raio entre dois pontos e retorna o primeiro objeto atingido.
        Útil para Visão de IA e Sensores.
        """
        # Quantidade de passos para verificar o raio (precisão)
        distancia = math.hypot(destino_x - origem_x, destino_y - origem_y)
        passos = int(distancia / 4) # Verifica a cada 4 pixels
        
        if passos == 0: return None

        for i in range(passos):
            t = i / passos
            px = origem_x + (destino_x - origem_x) * t
            py = origem_y + (destino_y - origem_y) * t
            
            # Verifica se este ponto do raio está dentro de algum sólido
            for solido in lista_solidos:
                if (solido.x <= px <= solido.x + solido.width and
                    solido.y <= py <= solido.y + solido.height):
                    return solido # Retorna o objeto atingido
        return None
    
    
    def draw_debug_circle(self, obj, cor=(255, 0, 0)):
        """Desenha o círculo de colisão para fins de debug."""
        from .window import Window
        raio = int(obj.width / 2)
        centro = (int(obj.x + raio), int(obj.y + raio))
        pygame.draw.circle(Window.get_screen(), cor, centro, raio, 1)