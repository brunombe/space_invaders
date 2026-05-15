from PPlay.sprite import *

def cor(janela, string):
    if string == "roxinho":
        return janela.set_background_color([15,0,20])
    elif string == "vermelho":
        return janela.set_background_color([200,0,20])
    elif string == "cinza":
        return janela.set_background_color([154,160,156])