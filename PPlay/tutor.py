"""
===============================================================================
POWER PPLAY 2.0 - TUTOR INTERATIVO OMNI-MASTER
===============================================================================
Desenvolvido por: Kauã Neves Jesus de Paula
Arquitetura: Desenvolvedor Sênior (IA)
Instituição: IC-UFF (2026)
===============================================================================
Este é um sistema de ajuda in-built que ensina a utilizar todos os módulos
da engine através do terminal.
===============================================================================
"""

import os
import sys

# Configuração de Cores para o Terminal
C = '\033[96m'  # Ciano (Títulos)
Y = '\033[93m'  # Amarelo (Código/Passos)
G = '\033[92m'  # Verde (Dicas Sênior)
R = '\033[91m'  # Vermelho (Alertas)
W = '\033[0m'   # Branco (Reset)
B = '\033[1m'   # Bold

def limpar():
    os.system('cls' if os.name == 'nt' else 'clear')

MENU_PRINCIPAL = f"""
{C}{B}╔══════════════════════════════════════════════════════════╗
║        BEM-VINDO AO MENTOR VIRTUAL - POWER PPLAY 2.0       ║
╚══════════════════════════════════════════════════════════╝{W}
{G}Selecione um módulo para aprender a implementar:{W}

[1]  {C}FUNDAMENTOS{W}  (Window, Tempo e Delta Time)
[2]  {C}INPUTS{W}       (Teclado, Mouse e Ações)
[3]  {C}ENTIDADES{W}    (Sprites e Animações)
[4]  {C}FÍSICA{W}       (Gravidade, Colisão e Feeling)
[5]  {C}MUNDO{W}        (Camera, TileMap e Parallax)
[6]  {C}ORGANIZAÇÃO{W}  (ObjectGroups e SceneManager)
[7]  {C}JUICE{W}        (Luz, Partículas, Shake e Flash)
[8]  {C}ALGORITMOS{W}   (Pathfinding A*, Tweens e Raycast)
[9]  {C}ARCHITECT{W}   (Automação de Arquivos)

[0]  {R}SAIR DO TUTOR{W}
"""

CONTEUDO = {
    "1": {
        "titulo": "A JANELA E O TEMPO",
        "corpo": f"""
O ponto de partida de qualquer jogo. A Window gerencia o canvas virtual.

{Y}# Como inicializar:{W}
janela = Window(800, 600, "Título do Jogo", pixel_art=True)

{Y}# No final do loop 'while True':{W}
janela.update()

{G}💡 DICA DO SÊNIOR:{W}
Nunca use valores fixos para movimento como 'x += 5'.
Sempre use: {Y}objeto.x += velocidade * janela.delta_time(){W}
Isso garante que o jogo rode na mesma velocidade em qualquer PC!
"""
    },
    "2": {
        "titulo": "ENTRADAS (INPUTS)",
        "corpo": f"""
A Power PPlay 2.0 separa o hardware da sua intenção.

{Y}# Teclado Dinâmico:{W}
if janela.keyboard.key_pressed("SPACE"): # Ativo enquanto segura
if janela.keyboard.key_down("ENTER"):    # Ativo apenas no clique

{Y}# Action Mapping (Mapeamento Profissional):{W}
InputManager.define_action("pulo", ["SPACE", "W", "UP"])
if InputManager.action_pressed("pulo"):
    player.jump()

{G}💡 DICA DO SÊNIOR:{W}
Use 'action_pressed' para ações únicas (atirar, pular) e 
'is_active' para movimentos contínuos (correr).
"""
    },
    "3": {
        "titulo": "SPRITES E ANIMAÇÕES",
        "corpo": f"""
Sprites são os 'atores' do jogo. Eles possuem quadros e imagens.

{Y}# Criando um personagem animado:{W}
player = Sprite("heroi.png", 4) # 4 frames horizontais
player.set_total_duration(500)   # 0.5 segundos de animação

{Y}# Métodos úteis:{W}
player.draw()             # Desenha na tela (respeita a câmera)
player.update()           # Troca os frames da animação
player.set_curr_frame(2)  # Muda para um frame específico
"""
    },
    "4": {
        "titulo": "FÍSICA CINEMÁTICA 4.0",
        "corpo": f"""
Adeus bugs de quinas! Nosso motor usa Separação de Eixos e Sub-stepping.

{Y}# Configuração:{W}
motor = Physics(gravidade=2500)
player.setup_physics(motor)

{Y}# No loop principal:{W}
# Resolve movimento, gravidade e colisão em 1 linha!
player.update_physics(lista_de_solidos)

{G}💡 DICA DO SÊNIOR:{W}
Ao usar 'update_physics', o player ganha automaticamente:
- {C}Coyote Time{W}: Pular um pouco depois de sair da plataforma.
- {C}Jump Buffer{W}: Aperte o botão antes de cair e ele pula ao tocar o chão.
"""
    },
    "5": {
        "titulo": "MUNDO GIGANTE E CÂMERA",
        "corpo": f"""
Não se limite ao tamanho da janela.

{Y}# Camera Suave:{W}
cam = Camera(1280, 720)
cam.follow(player, suavizacao=0.1)

{Y}# TileMap (Mapas em TXT):{W}
mapa = TileMap(40) # blocos de 40px
mapa.carregar_mapa("fase.txt", mapping)
mapa.draw() # Só desenha o que aparece na tela (Culling!)

{Y}# Parallax (Profundidade):{W}
parallax.add_layer("nuvens.png", 0.2) # Move a 20% da velocidade
"""
    },
    "6": {
        "titulo": "GESTÃO DE OBJETOS (GRUPOS)",
        "corpo": f"""
Ideal para quem não quer gerenciar listas complexas (for loops).

{Y}# Criando uma horda de inimigos:{W}
inimigos = ObjectGroup()
inimigos.add(Sprite("zumbi.png"))

{Y}# Comandos Coletivos:{W}
inimigos.draw()   # Desenha todos de uma vez
inimigos.update() # Anima todos de uma vez

{Y}# Colisão Mágica:{W}
atingido = inimigos.collided(player) # Retorna quem foi atingido
"""
    },
    "7": {
        "titulo": "GAME JUICE (EFEITOS)",
        "corpo": f"""
O que torna o jogo 'gostoso' de jogar.

{Y}# Screen Shake (Tremor):{W}
ScreenEffects.shake(intensidade=10, tempo=0.3)

{Y}# Lighting (Iluminação):{W}
luzes = LightingSystem()
luzes.lights.append((x, y, raio, brilho))
luzes.draw()

{Y}# Partículas (Explosões):{W}
emissor.set_pos(x, y)
emissor.explodir(30)
"""
    },
    "8": {
        "titulo": "INTELIGÊNCIA E ALGORITMOS",
        "corpo": f"""
A ciência da computação aplicada ao jogo.

{Y}# Pathfinding A*:{W}
caminho = Navigation.encontrar_caminho(mapa, start, goal)

{Y}# Raycasting (Visão de IA):{W}
visto = Collision.raycast(drone.x, drone.y, player.x, player.y, solidos)

{Y}# Tweens (Transições Suaves):{W}
Tween.to(botao, "x", 500, 1.0, "bounce") # Desliza quicando
"""
    },
    "9": {
        "titulo": "PPLAY ARCHITECT",
        "corpo": f"""
Organize seu projeto automaticamente pelo terminal.

{Y}# Comando:{W}
python PPlay/architect.py main.py NomeDaClasse pasta_destino

{G}O que ele faz:{W}
1. Recorta o código da sua classe do main.py.
2. Cria o arquivo na pasta nova.
3. Configura os Imports necessários.
4. Escreve o Import automático no seu main.py.
"""
    }
}

def rodar_tutor():
    while True:
        limpar()
        print(MENU_PRINCIPAL)
        escolha = input(f"{Y}Escolha um tópico (0 para sair): {W}")
        
        if escolha == "0":
            print(f"\n{G}Power PPlay 2.0 - Boa sorte no seu desenvolvimento, Líder!{W}\n")
            break
            
        if escolha in CONTEUDO:
            limpar()
            data = CONTEUDO[escolha]
            print(f"{C}{B}=== {data['titulo']} ==={W}")
            print(data["corpo"])
            input(f"\n{G}Pressione ENTER para voltar ao menu...{W}")
        else:
            print(f"{R}Opção inválida!{W}")
            

if __name__ == "__main__":
    rodar_tutor()