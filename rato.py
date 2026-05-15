from PPlay.mouse import*
mouse = Mouse()
def clicou_em(obj):
    if mouse.button_pressed(1):
        click = 1
    else: 
        click = 0
    antes = click
    if mouse.is_over_object(obj) and click == 1 and antes == 0:
        return 1
    else:
        return 0
    

    