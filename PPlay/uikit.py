import pygame
from .window import Window
from .gameobject import GameObject

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

class Button(GameObject):
    """
    Um botão interativo que suporta cores, texto e estados de hover.
    """
    def __init__(self, largura, altura, texto="", cor_base="gray", cor_hover="lightgray"):
        super().__init__()
        self.width = largura
        self.height = altura
        self.texto = texto
        
        # Cores (podem ser tuplas RGB ou Strings)
        self.cor_base = pygame.Color(cor_base) if isinstance(cor_base, str) else cor_base
        self.cor_hover = pygame.Color(cor_hover) if isinstance(cor_hover, str) else cor_hover
        self.cor_texto = (255, 255, 255)
        
        self.hovered = False
        self.pressed = False

    def update(self):
        """Atualiza o estado do botão baseado no mouse."""
        mouse = Window.get_instance().mouse
        
        # Verifica se o mouse está sobre o botão (usa coordenadas virtuais)
        if mouse.is_over_object(self):
            self.hovered = True
            # Se clicou com o botão esquerdo
            if mouse.button_down(mouse.LEFT):
                self.pressed = True
            else:
                self.pressed = False
        else:
            self.hovered = False
            self.pressed = False

    def is_clicked(self):
        """Retorna True apenas no frame em que o botão foi clicado."""
        mouse = Window.get_instance().mouse
        return mouse.is_over_object(self) and mouse.button_down(mouse.LEFT)

    def draw(self):
        """Desenha o botão com feedback visual de hover."""
        cor = self.cor_hover if self.hovered else self.cor_base
        # Se estiver pressionado, escurece um pouco a cor
        if self.pressed:
            cor = [max(0, c - 40) for c in cor] if not isinstance(cor, pygame.Color) else cor

        # Desenha o corpo do botão no buffer virtual
        screen = Window.get_screen()
        pygame.draw.rect(screen, cor, (self.x, self.y, self.width, self.height))
        # Borda sutil
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height), 1)

        # Desenha o texto centralizado
        if self.texto:
            # Usamos o draw_text da janela, mas calculamos o centro
            # Para simplificar, vamos renderizar uma fonte interna aqui
            fonte = pygame.font.SysFont("Arial", 20)
            img_texto = fonte.render(self.texto, True, self.cor_texto)
            tx = self.x + (self.width - img_texto.get_width()) / 2
            ty = self.y + (self.height - img_texto.get_height()) / 2
            screen.blit(img_texto, (tx, ty))

class ProgressBar(GameObject):
    """
    Barra de progresso visual (Vida, Mana, Carregamento).
    """
    def __init__(self, largura, altura, cor_barra="red", cor_fundo="black"):
        super().__init__()
        self.width = largura
        self.height = altura
        self.cor_barra = cor_barra
        self.cor_fundo = cor_fundo
        self.valor_max = 100
        self.valor_atual = 100

    def set_value(self, valor):
        self.valor_atual = max(0, min(valor, self.valor_max))

    def draw(self):
        screen = Window.get_screen()
        # Desenha o fundo
        pygame.draw.rect(screen, self.cor_fundo, (self.x, self.y, self.width, self.height))
        
        # Calcula a largura da barra preenchida
        largura_preenchida = (self.valor_atual / self.valor_max) * self.width
        
        # Desenha o preenchimento
        if largura_preenchida > 0:
            pygame.draw.rect(screen, self.cor_barra, (self.x, self.y, largura_preenchida, self.height))
        
        # Borda
        pygame.draw.rect(screen, (200, 200, 200), (self.x, self.y, self.width, self.height), 1)