"""
===============================================================================
POWER PPLAY 2.0 - RETRO-COMPATIBILITY BRIDGE v2.2
===============================================================================
Correção de Métodos de Classe e Atributos Estáticos.
Mapeia o comportamento da 1.0 injetando lógica na 2.0.
===============================================================================
"""
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

def aplicar_retrocompatibilidade():
    try:
        from .window import Window
        from .mouse import Mouse
        from .keyboard import Keyboard
        from .animation import Animation
        from .sound import Sound
        from .sprite import Sprite
        from .gameimage import GameImage
        from .collision import Collision
    except ImportError:
        return

    # --- 1. WINDOW: TRADUÇÃO DE ATRIBUTOS E CLASSMETHODS ---
    
    # Redireciona Window.width -> Window.largura (Instância)
    Window.width = property(lambda self: self.largura)
    Window.height = property(lambda self: self.altura)

    # Injeção de Métodos de Classe (Corrigindo o erro de missing 'cls')
    Window.get_keyboard = classmethod(lambda cls: cls.get_instance().keyboard)
    Window.get_mouse = classmethod(lambda cls: cls.get_instance().mouse)
    
    # Métodos de Instância Legados
    Window.set_title = lambda self, t: pygame.display.set_caption(t)
    Window.delay = lambda self, ms: pygame.time.delay(ms)
    Window.time_elapsed = lambda self: pygame.time.get_ticks()
    Window.clear = lambda self: [self.set_background_color((255,255,255)), self.update()]

    # Draw Text Híbrido (Suporte a color/size/bold/italic da 1.0)
    def draw_text_compat(self, text, x, y, **kwargs):
        size = kwargs.get('size', kwargs.get('tamanho', 12))
        color = kwargs.get('color', kwargs.get('cor', (0,0,0)))
        font_name = kwargs.get('font_name', kwargs.get('fonte', "Arial"))
        bold = kwargs.get('bold', False)
        italic = kwargs.get('italic', False)
        f = pygame.font.SysFont(font_name, size, bold, italic)
        self.screen.blit(f.render(str(text), True, color), [x, y])
    Window.draw_text = draw_text_compat

    # --- 2. INPUTS: TRADUÇÃO DE TECLAS E BOTÕES ---
    # Algumas versões da 1.0 aceitavam 'LEFT' (string) ou constantes. 
    # Nossa 2.0 já trata strings, então aqui apenas mapeamos métodos.
    Keyboard.key_pressed_legacy = lambda self, k: self.key_pressed(k)
    # Patch para o método show_key_pressed que o PPlay 1.0 possuía
    def show_key_legacy(self):
        for e in Window.get_instance().eventos:
            if e.type == pygame.KEYDOWN: print(e.key)
    Keyboard.show_key_pressed = show_key_legacy

    # Constantes do Mouse
    Mouse.BUTTON_LEFT = 1; Mouse.BUTTON_MIDDLE = 2; Mouse.BUTTON_RIGHT = 3
    Mouse.WHEEL_UP = 4; Mouse.WHEEL_DOWN = 5
    # Traduz click.is_button_pressed(True) -> click.button_pressed(1)
    Mouse.is_button_pressed = lambda self, b: self.button_pressed(1 if b is True else b)
    Mouse.set_position = lambda self, x, y: pygame.mouse.set_pos([x, y])
    Mouse.hide = lambda self: pygame.mouse.set_visible(False)
    Mouse.unhide = lambda self: pygame.mouse.set_visible(True)
    Mouse.is_over_area = lambda self, sp, ep: (sp[0] <= self.get_position()[0] <= ep[0]) and (sp[1] <= self.get_position()[1] <= ep[1])

    # --- 3. ANIMAÇÃO E SPRITE ---
    # Traduz o sistema de fatiamento de tempo da 1.0
    def set_sequence_time_legacy(self, start, end, duration, loop=True):
        self.set_total_duration(duration)
        self.set_loop(loop)
        self.frame_atual = start

    Animation.set_sequence_time = set_sequence_time_legacy
    Animation.set_sequence = lambda self, s, e, l=True: self.set_loop(l)
    Animation.set_curr_frame = lambda self, f: setattr(self, 'frame_atual', f)
    Animation.hide = lambda self: setattr(self, 'drawable', False)
    Animation.unhide = lambda self: setattr(self, 'drawable', True)

    # --- 4. COLISÃO E IMAGEM ---
    Collision.collided_perfect = lambda obj1, obj2: Collision.perfect_collision(obj1, obj2)
    GameImage.collided_perfect = lambda self, target: Collision.perfect_collision(self, target)

    print("[Power PPlay 2.0] Ponte v2.2 ativa: Métodos de classe vinculados.")

# Ativação imediata
aplicar_retrocompatibilidade()