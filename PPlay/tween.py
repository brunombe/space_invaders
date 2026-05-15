import math
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

class Tween:
    """
    Gerenciador de Interpolação (Juice). 
    Faz transições suaves em qualquer atributo de um objeto.
    """
    _ativos = []

    @classmethod
    def to(cls, objeto, atributo, valor_final, duracao, tipo="linear"):
        """
        Interpola um atributo do objeto até o valor final.
        Tipos: 'linear', 'ease_in', 'ease_out', 'bounce'
        """
        valor_inicial = getattr(objeto, atributo)
        cls._ativos.append({
            "obj": objeto,
            "attr": atributo,
            "ini": valor_inicial,
            "fim": valor_final,
            "dur": duracao,
            "progresso": 0,
            "tipo": tipo
        })

    @classmethod
    def update(cls):
        dt = Window.get_instance().delta_time()
        for t in cls._ativos[:]:
            t["progresso"] += dt / t["dur"]
            p = min(1.0, t["progresso"])
            
            # Funções de Easing (Matemática Pura)
            if t["tipo"] == "ease_in":
                f = p * p
            elif t["tipo"] == "ease_out":
                f = 1 - (1 - p) * (1 - p)
            elif t["tipo"] == "bounce":
                # Efeito de rebote simples
                f = 1 - abs(math.cos(p * math.pi * 2) * (1 - p))
            else: # Linear
                f = p
            
            novo_valor = t["ini"] + (t["fim"] - t["ini"]) * f
            setattr(t["obj"], t["attr"], novo_valor)
            
            if p >= 1.0:
                cls._ativos.remove(t)