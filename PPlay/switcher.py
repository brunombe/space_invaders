"""
===============================================================================
PPLAY VERSION SWITCHER (TIME MACHINE)
===============================================================================
Alterna entre a Power PPlay 2.0 (NEOP) e a PPlay 1.0 Original (LEGACY).
Uso no terminal: python PPlay/switcher.py
===============================================================================
"""

import os
import shutil
import sys

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

class VersionManager:
    def __init__(self):
        # Define os caminhos absolutos
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.legacy_dir = os.path.join(self.base_dir, "legacy")
        self.neop_dir = os.path.join(self.base_dir, "neop")
        
        # Arquivos utilitários que NUNCA devem ser movidos
        self.ignore_list =["switcher.py", "architect.py", "__pycache__"]

        # Garante que as pastas existam
        os.makedirs(self.legacy_dir, exist_ok=True)
        os.makedirs(self.neop_dir, exist_ok=True)

    def get_active_version(self):
        """Descobre qual versão está na raiz procurando por features exclusivas da 2.0."""
        # Se 'scenemanager.py' ou 'uikit.py' existem na raiz, estamos na 2.0 (NEOP)
        if os.path.exists(os.path.join(self.base_dir, "scenemanager.py")):
            return "NEOP"
        return "LEGACY"

    def move_files(self, origem, destino):
        """Move todos os arquivos .py de uma pasta para outra."""
        movidos = 0
        for item in os.listdir(origem):
            if item.endswith(".py") and item not in self.ignore_list:
                caminho_origem = os.path.join(origem, item)
                caminho_destino = os.path.join(destino, item)
                shutil.move(caminho_origem, caminho_destino)
                movidos += 1
        return movidos

    def check_folder_has_files(self, folder):
        """Verifica se a pasta tem arquivos .py para serem restaurados."""
        for item in os.listdir(folder):
            if item.endswith(".py"): return True
        return False

    def swap(self):
        print("\n" + "="*50)
        print("PPLAY VERSION SWITCHER".center(50))
        print("="*50)

        current_version = self.get_active_version()

        if current_version == "NEOP":
            print("[!] Versão Ativa Detectada: POWER PPLAY 2.0 (NEOP)")
            
            if not self.check_folder_has_files(self.legacy_dir):
                print("\n[ERRO] A pasta 'PPlay/legacy/' está vazia!")
                print("Por favor, coloque os arquivos do PPlay 1.0 lá dentro antes de fazer a troca.")
                print("="*50 + "\n")
                return

            print("-> Guardando PPlay 2.0 na pasta '/neop/'.")
            self.move_files(self.base_dir, self.neop_dir)
            
            print("-> Restaurando PPlay 1.0 da pasta '/legacy/'.")
            self.move_files(self.legacy_dir, self.base_dir)
            
            print("\n[SUCESSO] A engine foi revertida para a versão LEGACY (1.0).")

        else:
            print("[!] Versão Ativa Detectada: PPLAY 1.0 (LEGACY)")
            
            if not self.check_folder_has_files(self.neop_dir):
                print("\n[ERRO] A pasta 'PPlay/neop/' está vazia!")
                print("Não há versão 2.0 salva para restaurar.")
                print("="*50 + "\n")
                return

            print("-> Guardando PPlay 1.0 na pasta '/legacy/'.")
            self.move_files(self.base_dir, self.legacy_dir)
            
            print("-> Restaurando Power PPlay 2.0 da pasta '/neop/'.")
            self.move_files(self.neop_dir, self.base_dir)
            
            print("\n[SUCESSO] A engine foi atualizada para a versão NEOP (2.0).")
            
        print("="*50 + "\n")

if __name__ == "__main__":
    manager = VersionManager()
    manager.swap()