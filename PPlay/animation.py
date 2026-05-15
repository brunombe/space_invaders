import pygame
from .gameimage import GameImage
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


class Animation(GameImage):
    """
    Gerencia sequências de frames (Spritesheets) com controle de tempo
    baseado em Delta Time e suporte a Câmera.
    """
    def __init__(self, caminho_imagem, total_frames, loop=True):
        super().__init__(caminho_imagem)
        
        self.total_frames = total_frames
        self.loop = loop
        
        # Ajusta a largura para o tamanho de UM frame
        self.width = self.width / total_frames
        
        self.frame_atual = 0
        self.rodando = True
        
        # Controle de tempo (em segundos)
        self.tempo_por_frame = 0.1  # Padrão: 10 FPS
        self.tempo_acumulado = 0

    def set_total_duration(self, tempo_total_ms):
        """Define a duração total de uma volta completa da animação."""
        tempo_total_seg = tempo_total_ms / 1000.0
        self.tempo_por_frame = tempo_total_seg / self.total_frames

    def set_curr_frame(self, frame):
        """Define manualmente o frame atual (0 até total_frames - 1)."""
        if 0 <= frame < self.total_frames:
            self.frame_atual = frame

    def get_curr_frame(self):
        """Retorna o índice do frame sendo exibido."""
        return self.frame_atual

    def set_loop(self, loop):
        """Define se a animação deve recomeçar ao chegar no fim."""
        self.loop = loop

    def update(self):
        """Troca os frames baseando-se no tempo real transcorrido (Delta Time)."""
        if not self.rodando:
            return

        self.tempo_acumulado += Window.get_instance().delta_time()

        if self.tempo_acumulado >= self.tempo_por_frame:
            self.frame_atual += 1
            self.tempo_acumulado = 0

            if self.frame_atual >= self.total_frames:
                if self.loop:
                    self.frame_atual = 0
                else:
                    self.frame_atual = self.total_frames - 1
                    self.rodando = False

    def draw(self):
        """Desenha o frame atual aplicando transformações e suporte a Câmera."""
        cam = Camera.get_instance()
        
        # Coordenadas virtuais para suporte a Câmera
        draw_x = cam.transform_x(self.x) if cam else self.x
        draw_y = cam.transform_y(self.y) if cam else self.y

        # Define o retângulo de corte na Spritesheet
        area_corte = pygame.Rect(
            self.frame_atual * self.width, 0,
            self.width, self.height
        )
        
        # Extrai o frame da spritesheet
        frame_surface = self.image.subsurface(area_corte).copy()
        
        # Aplica transparência
        frame_surface.set_alpha(self.transparency)
        
        # Aplica rotação
        if self.rotation != 0:
            frame_surface = pygame.transform.rotate(frame_surface, self.rotation)
        
        # Aplica escala
        if self.scale_x != 1.0 or self.scale_y != 1.0:
            nova_w = max(1, int(self.width * self.scale_x))
            nova_h = max(1, int(self.height * self.scale_y))
            frame_surface = pygame.transform.scale(frame_surface, (nova_w, nova_h))
        
        # Desenha apenas o pedaço (frame) transformado no buffer virtual
        Window.get_screen().blit(frame_surface, (draw_x, draw_y))

    def play(self): self.rodando = True
    def stop(self): self.rodando = False; self.frame_atual = 0
    def pause(self): self.rodando = False