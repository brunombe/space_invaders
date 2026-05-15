import pygame
import sys
from pygame.locals import *

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

class Window:
    """
    POWER PPLAY 2.0 - Janela de Alta Performance e Resolução Virtual.
    Versão 2.6.2: Blindada contra erros de escalonamento e minimização.
    """
    _instance = None 
    screen = None # Atributo estático para compatibilidade legada

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Window, cls).__new__(cls)
        return cls._instance

    def __init__(self, largura_virtual=800, altura_virtual=600, titulo="Power PPlay 2.0", resizavel=True, pixel_art=True):
        if hasattr(self, '_already_init'):
            return
        
        if not pygame.get_init():
            pygame.init()

        # Resolução interna do jogo
        self.largura = largura_virtual
        self.altura = altura_virtual
        self.titulo = titulo
        self.pixel_art = pixel_art
        
        self._clock = pygame.time.Clock()
        self._delta_time = 0
        self.eventos = []
        self.cor_fundo = (0, 0, 0)

        # Configura flags de vídeo
        flags = pygame.DOUBLEBUF | pygame.HWSURFACE
        if resizavel:
            flags |= pygame.RESIZABLE
            
        # Cria a janela real do Windows
        self.real_screen = pygame.display.set_mode([self.largura, self.altura], flags)
        
        # Cria o Buffer Virtual (Canvas)
        self.screen = pygame.Surface((self.largura, self.altura))
        Window.screen = self.screen # Sincroniza atributo estático
        
        pygame.display.set_caption(self.titulo)
        
        # Subsistemas
        from .keyboard import Keyboard
        from .mouse import Mouse
        self.keyboard = Keyboard()
        self.mouse = Mouse()
        
        self._already_init = True

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            Window()
        return cls._instance

    @classmethod
    def get_screen(cls):
        return cls.get_instance().screen

    def update(self):
        """Finaliza o desenho e projeta na tela real com proteção contra crash."""
        largura_real, altura_real = self.real_screen.get_size()
        
        # PROTEÇÃO: Se a janela estiver minimizada (tamanho 0), não tenta desenhar
        if largura_real < 1 or altura_real < 1:
            pygame.display.flip()
            self._clock.tick()
            self.eventos = pygame.event.get()
            return

        # Cálculo do escalonamento mantendo Aspect Ratio
        ratio = min(largura_real / self.largura, altura_real / self.altura)
        nova_w = max(1, int(self.largura * ratio))
        nova_h = max(1, int(self.altura * ratio))
        pos_x = (largura_real - nova_w) // 2
        pos_y = (altura_real - nova_h) // 2
        
        # Preenche fundo (faixas pretas)
        self.real_screen.fill((0, 0, 0))
        
        # Tenta realizar o redimensionamento com tratamento de erro
        try:
            if self.pixel_art:
                scaled = pygame.transform.scale(self.screen, (nova_w, nova_h))
            else:
                scaled = pygame.transform.smoothscale(self.screen, (nova_w, nova_h))
            
            self.real_screen.blit(scaled, (pos_x, pos_y))
        except pygame.error:
            # Fallback caso o transform falhe por algum motivo de hardware
            self.real_screen.blit(self.screen, (0, 0))
            
        pygame.display.flip()
        
        # Limpa o buffer para o próximo frame
        self.screen.fill(self.cor_fundo)
        
        # Eventos
        self.eventos = pygame.event.get()
        for ev in self.eventos:
            if ev.type == QUIT:
                self.close()
            if ev.type == KEYDOWN and ev.key == K_F11:
                pygame.display.toggle_fullscreen()

        # Sincroniza o tempo (Delta Time)
        self._delta_time = self._clock.tick() / 1000.0

    def delta_time(self):
        return self._delta_time

    def get_fps(self):
        return self._clock.get_fps()

    def set_background_color(self, cor):
        if isinstance(cor, str):
            try: self.cor_fundo = pygame.Color(cor)
            except: self.cor_fundo = (0,0,0)
        else:
            self.cor_fundo = cor

    def draw_text(self, texto, x, y, tamanho=20, cor=(255, 255, 255), fonte="Arial"):
        try:
            f = pygame.font.SysFont(fonte, tamanho)
            img = f.render(str(texto), True, cor)
            self.screen.blit(img, (x, y))
        except: pass

    def screen_to_virtual_coords(self, px, py):
        lw, lh = self.real_screen.get_size()
        if lw < 1 or lh < 1: return px, py
        ratio = min(lw / self.largura, lh / self.altura)
        vx = (px - (lw - self.largura * ratio) // 2) / ratio
        vy = (py - (lh - self.altura * ratio) // 2) / ratio
        return vx, vy

    def close(self):
        pygame.quit()
        sys.exit()