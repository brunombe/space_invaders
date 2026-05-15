import pygame
import os

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

class SoundManager:
    """
    Gerenciador estático de áudio. Controla volumes globais e canais.
    """
    _sfx_cache = {}
    _volume_sfx = 1.0  # 0.0 a 1.0
    _volume_music = 1.0

    @classmethod
    def inicializar(cls):
        if not pygame.mixer.get_init():
            # Configuração de alta fidelidade e baixa latência
            pygame.mixer.pre_init(44100, -16, 2, 512)
            pygame.mixer.init()

    @classmethod
    def set_sfx_volume(cls, volume):
        """Define o volume de todos os efeitos sonoros (0 a 100)."""
        cls._volume_sfx = volume / 100.0
        for sfx in cls._sfx_cache.values():
            sfx.set_volume(cls._volume_sfx)

    @classmethod
    def set_music_volume(cls, volume):
        """Define o volume da música de fundo (0 a 100)."""
        cls._volume_music = volume / 100.0
        pygame.mixer.music.set_volume(cls._volume_music)

class Sound:
    """
    Classe para Efeitos Sonoros (SFX) curtos.
    Carregados na RAM para execução instantânea.
    """
    def __init__(self, caminho_arquivo):
        SoundManager.inicializar()
        
        # Sistema de Cache de Áudio
        if caminho_arquivo in SoundManager._sfx_cache:
            self.sound = SoundManager._sfx_cache[caminho_arquivo]
        else:
            if os.path.exists(caminho_arquivo):
                self.sound = pygame.mixer.Sound(caminho_arquivo)
                SoundManager._sfx_cache[caminho_arquivo] = self.sound
            else:
                print(f"ERRO: Arquivo de som não encontrado: {caminho_arquivo}")
                self.sound = None

        if self.sound:
            self.sound.set_volume(SoundManager._volume_sfx)

    def play(self, repetições=0):
        """Toca o som. repetições=-1 para loop infinito."""
        if self.sound:
            self.sound.play(loops=repetições)

    def stop(self):
        if self.sound:
            self.sound.stop()

    def set_volume(self, volume_percentual):
        """Define o volume deste som específico (0 a 100)."""
        if self.sound:
            self.sound.set_volume(volume_percentual / 100.0)

class Music:
    """
    Classe para Música de Fundo (BGM).
    Lida via streaming para economizar memória.
    """
    def __init__(self, caminho_arquivo):
        SoundManager.inicializar()
        self.caminho = caminho_arquivo

    def play(self, loops=-1, fade_in_ms=2000):
        """Toca a música com efeito de fade-in opcional."""
        if os.path.exists(self.caminho):
            pygame.mixer.music.load(self.caminho)
            pygame.mixer.music.set_volume(SoundManager._volume_music)
            pygame.mixer.music.play(loops=loops, fade_ms=fade_in_ms)
        else:
            print(f"ERRO: Arquivo de música não encontrado: {self.caminho}")

    def stop(self, fade_out_ms=1000):
        pygame.mixer.music.fadeout(fade_out_ms)

    def pause(self):
        pygame.mixer.music.pause()

    def unpause(self):
        pygame.mixer.music.unpause()

    def is_playing(self):
        return pygame.mixer.music.get_busy()