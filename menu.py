import pygame,pygame_menu
from main import *
from settings1 import *

pygame.init()
surface = pygame.display.set_mode((WIDTH, HEIGHT))

def stage(self, value):
    print("STAGE :value")

def start():
    print("Game Start")
    Game()

pygame_set=pygame_menu.themes.THEME_DARK;
pygame_set.widget_font=pygame.font.SysFont("gulim",30)
menu=pygame_menu.Menu("Menu",400,300,theme=pygame_set)

menu.add.selector("STAGE", [("STAGE1", 1), ("STAGE2", 2)], onchange=stage)
menu.add.button("Game START", start)
menu.add.button("Game Exit", pygame_menu.events.EXIT)
menu.mainloop(surface)