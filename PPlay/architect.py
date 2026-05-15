import ast
import os
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


class ProjectArchitect:
    """
    Ferramenta de Automação de Estrutura da PPlay 2.0.
    Localizada em: projeto/PPlay/architect.py
    Executada de: projeto/
    """

    @staticmethod
    def modularize(arquivo_origem, nome_entidade, pasta_destino="scripts"):
        # Obtém o caminho absoluto da pasta onde o usuário está (raiz do projeto)
        raiz_projeto = os.getcwd()
        caminho_origem = os.path.join(raiz_projeto, arquivo_origem)
        
        if not os.path.exists(caminho_origem):
            print(f"ERRO: O arquivo '{arquivo_origem}' não foi encontrado na raiz do projeto.")
            return

        # 1. Cria a pasta de destino na raiz do projeto
        caminho_pasta_destino = os.path.join(raiz_projeto, pasta_destino)
        if not os.path.exists(caminho_pasta_destino):
            os.makedirs(caminho_pasta_destino)
            with open(os.path.join(caminho_pasta_destino, "__init__.py"), "w") as f:
                pass

        # 2. Lê o código fonte
        with open(caminho_origem, "r", encoding="utf-8") as f:
            source = f.read()

        # 3. Analisa a árvore de sintaxe (AST)
        try:
            tree = ast.parse(source)
        except SyntaxError as e:
            print(f"ERRO de Sintaxe no arquivo original: {e}")
            return

        entidade_node = None
        for node in ast.walk(tree):
            if (isinstance(node, (ast.ClassDef, ast.FunctionDef)) and node.name == nome_entidade):
                entidade_node = node
                break

        if not entidade_node:
            print(f"ERRO: Entidade '{nome_entidade}' não encontrada em '{arquivo_origem}'.")
            return

        # 4. Extrai o código
        linhas = source.splitlines()
        inicio = entidade_node.lineno - 1
        fim = getattr(entidade_node, "end_lineno", len(linhas))
        codigo_extraido = "\n".join(linhas[inicio:fim])

        # 5. Salva no novo arquivo dentro da pasta escolhida
        nome_arquivo_novo = f"{nome_entidade.lower()}.py"
        caminho_final_novo = os.path.join(caminho_pasta_destino, nome_arquivo_novo)
        
        # Cabeçalho padrão para garantir que os componentes da PPlay funcionem
        # Nota: Usamos "from PPlay.window" assumindo que a PPlay está na raiz
        headers = (
            f"# Arquivo gerado automaticamente pelo PPlay 2.0 Architect\n"
            f"from PPlay.window import Window\n"
            f"from PPlay.sprite import Sprite\n"
            f"from PPlay.gameimage import GameImage\n\n"
        )
        
        with open(caminho_final_novo, "w", encoding="utf-8") as f:
            f.write(headers + codigo_extraido)

        # 6. Atualiza o arquivo original (Remove a classe e adiciona o import)
        linhas_restantes = linhas[:inicio] + linhas[fim:]
        
        # Adiciona o import no topo apontando para a nova pasta
        linha_import = f"from {pasta_destino}.{nome_entidade.lower()} import {nome_entidade}"
        
        # Evita duplicar o import caso o usuário rode o comando duas vezes
        if linha_import not in linhas_restantes:
            linhas_restantes.insert(0, linha_import)

        with open(caminho_origem, "w", encoding="utf-8") as f:
            f.write("\n".join(linhas_restantes))

        print(f"\n[PPlay 2.0 Architect]")
        print(f"-> Entidade '{nome_entidade}' movida com sucesso!")
        print(f"-> Destino: {pasta_destino}/{nome_arquivo_novo}")
        print(f"-> Arquivo '{arquivo_origem}' atualizado com o novo import.\n")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("\n[PPlay 2.0 Architect] - Uso Incorreto")
        print("Exemplo: python PPlay/architect.py main.py NomeDaClasse nome_da_pasta")
    else:
        # Argumentos: 1: arquivo_origem, 2: classe, 3: pasta
        origem = sys.argv[1]
        classe = sys.argv[2]
        pasta = sys.argv[3] if len(sys.argv) > 3 else "scripts"
        ProjectArchitect.modularize(origem, classe, pasta)