import pygame
import random
from .window import Window
from .camera import Camera

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

class Particle:
    """
    Uma única partícula no sistema. 
    Contém posição, velocidade, cor e tempo de vida.
    """
    def __init__(self, x, y, vx, vy, vida, cor, tamanho):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.vida_max = vida
        self.vida_restante = vida
        self.cor = cor
        self.tamanho = tamanho

    def update(self, dt):
        """Atualiza posição e reduz vida."""
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vida_restante -= dt

    def esta_viva(self):
        return self.vida_restante > 0

class ParticleEmitter:
    """
    O Emissor é a 'fonte' que cria e gerencia as partículas.
    Pode ser usado para fumaça, fogo, faíscas, etc.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.particulas = []
        
        # Configurações padrão
        self.cor = (255, 255, 255)
        self.tamanho_base = 4
        self.vida_base = 1.0 # segundos
        self.intensidade = 5 # partículas por emissão
        
        # Dispersão (Aleatoriedade)
        self.spread_x = 50
        self.spread_y = 50

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def emitir(self):
        """Cria novas partículas com base na intensidade."""
        for _ in range(self.intensidade):
            # Adiciona aleatoriedade na velocidade
            vx = random.uniform(-self.spread_x, self.spread_x)
            vy = random.uniform(-self.spread_y, self.spread_y)
            
            # Adiciona aleatoriedade na vida
            vida = random.uniform(self.vida_base * 0.5, self.vida_base * 1.5)
            
            nova_p = Particle(self.x, self.y, vx, vy, vida, self.cor, self.tamanho_base)
            self.particulas.append(nova_p)

    def update(self):
        """Atualiza todas as partículas e remove as mortas."""
        dt = Window.get_instance().delta_time()
        
        for p in self.particulas[:]: # Cópia da lista para remoção segura
            p.update(dt)
            if not p.esta_viva():
                self.particulas.remove(p)

    def draw(self):
        """Desenha as partículas considerando a câmera e transparência."""
        screen = Window.get_screen()
        cam = Camera.get_instance()
        
        for p in self.particulas:
            # Transparência baseada na vida restante (Fade out)
            alpha = int((p.vida_restante / p.vida_max) * 255)
            cor_com_alpha = (*p.cor, alpha)
            
            # Posição relativa à câmera
            dx = cam.transform_x(p.x) if cam else p.x
            dy = cam.transform_y(p.y) if cam else p.y
            
            # Desenha um pequeno círculo ou quadrado
            # Nota: pygame.draw não suporta alpha direto em superfícies comuns
            # Criamos uma pequena surface temporária para o efeito de fade
            p_surf = pygame.Surface((p.tamanho*2, p.tamanho*2), pygame.SRCALPHA)
            pygame.draw.circle(p_surf, cor_com_alpha, (p.tamanho, p.tamanho), p.tamanho)
            screen.blit(p_surf, (dx - p.tamanho, dy - p.tamanho))

    def explodir(self, quantidade=20):
        """Emite uma grande quantidade de uma vez (efeito impacto)."""
        temp_intensidade = self.intensidade
        self.intensidade = quantidade
        self.emitir()
        self.intensidade = temp_intensidade